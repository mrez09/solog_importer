import base64
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import pymysql
from pydantic import BaseModel, ConfigDict

from app.services.schema_snapshot import (
    TargetSchemaSnapshot,
    build_target_schema_snapshot,
    collect_schema_metadata,
)
from app.models.target_database import (
    PROTECTED_REFERENCE_DATABASE,
    TargetDatabaseProfile,
)

CONNECT_TIMEOUT_SECONDS = 5
FORM_TOKEN_TTL_SECONDS = 600
RESULT_CACHE_TTL_SECONDS = 1800

_FORM_TOKEN_SECRET = secrets.token_bytes(32)
_GRANT_PATTERN = re.compile(r"^GRANT\s+(.+?)\s+ON\s+(.+?)\s+TO\s+", re.IGNORECASE)

_TABLES_QUERY = """
SELECT TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = %s
ORDER BY TABLE_NAME
"""
_COLUMNS_QUERY = """
SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, EXTRA
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = %s
ORDER BY TABLE_NAME, ORDINAL_POSITION
"""
_PRIMARY_KEYS_QUERY = """
SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = %s AND CONSTRAINT_NAME = 'PRIMARY'
ORDER BY TABLE_NAME, ORDINAL_POSITION
"""
_FOREIGN_KEYS_QUERY = """
SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME,
       REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME, ORDINAL_POSITION
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, CONSTRAINT_NAME, ORDINAL_POSITION
"""
_UNIQUE_INDEXES_QUERY = """
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = %s AND NON_UNIQUE = 0 AND INDEX_NAME <> 'PRIMARY'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX
"""
_AUTO_INCREMENT_QUERY = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = %s AND EXTRA LIKE %s
GROUP BY TABLE_NAME
ORDER BY TABLE_NAME
"""


class ServerIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engine_version: str
    server_hostname: str
    server_port: int
    database: str
    authenticated_user: str
    effective_user: str


class ColumnDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table: str
    column: str
    column_type: str
    nullable: bool
    extra: str


class PrimaryKeyDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table: str
    columns: list[str]


class ForeignKeyDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table: str
    constraint: str
    columns: list[str]
    referenced_table: str
    referenced_columns: list[str]


class UniqueIndexDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table: str
    index: str
    columns: list[str]


class SchemaMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_table_count: int
    view_count: int
    column_count: int
    primary_key_count: int
    foreign_key_count: int
    unique_index_count: int
    auto_increment_table_count: int
    columns: list[ColumnDefinition]
    primary_keys: list[PrimaryKeyDefinition]
    foreign_keys: list[ForeignKeyDefinition]
    unique_indexes: list[UniqueIndexDefinition]
    auto_increment_tables: list[str]


class TargetDatabaseVerificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: UUID
    profile_fingerprint: str
    verified_at: str
    status: str
    statuses: list[str]
    message: str
    error_category: str | None = None
    identity: ServerIdentity | None = None
    privileges_status: str
    write_privileges_detected: bool = False
    schema_metadata: SchemaMetadata | None = None


def profile_fingerprint(profile: TargetDatabaseProfile) -> str:
    serialized = json.dumps(
        profile.model_dump(mode="json"),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def create_verification_form_token(
    profile: TargetDatabaseProfile,
    *,
    now: int | None = None,
) -> str:
    issued_at = int(time.time()) if now is None else now
    payload = json.dumps(
        {
            "profile_id": str(profile.profile_id),
            "fingerprint": profile_fingerprint(profile),
            "issued_at": issued_at,
            "nonce": secrets.token_urlsafe(16),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    signature = hmac.new(
        _FORM_TOKEN_SECRET,
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()
    return f"{encoded_payload}.{signature}"


def validate_verification_form_token(
    token: str,
    profile: TargetDatabaseProfile,
    *,
    now: int | None = None,
) -> bool:
    try:
        encoded_payload, supplied_signature = token.split(".", maxsplit=1)
        expected_signature = hmac.new(
            _FORM_TOKEN_SECRET,
            encoded_payload.encode("ascii"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(supplied_signature, expected_signature):
            return False
        padding = "=" * (-len(encoded_payload) % 4)
        payload: Any = json.loads(
            base64.urlsafe_b64decode(encoded_payload + padding)
        )
        issued_at = int(payload["issued_at"])
        current_time = int(time.time()) if now is None else now
        return (
            payload["profile_id"] == str(profile.profile_id)
            and hmac.compare_digest(
                str(payload["fingerprint"]),
                profile_fingerprint(profile),
            )
            and 0 <= current_time - issued_at <= FORM_TOKEN_TTL_SECONDS
        )
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        return False


class TargetDatabaseVerificationResultCache:
    def __init__(self) -> None:
        self._results: dict[
            UUID,
            tuple[float, str, TargetDatabaseVerificationResult],
        ] = {}
        self._lock = threading.Lock()

    def put(
        self,
        profile: TargetDatabaseProfile,
        result: TargetDatabaseVerificationResult,
    ) -> None:
        with self._lock:
            self._results[profile.profile_id] = (
                time.monotonic(),
                profile_fingerprint(profile),
                result,
            )

    def get(
        self,
        profile: TargetDatabaseProfile,
    ) -> TargetDatabaseVerificationResult | None:
        with self._lock:
            cached = self._results.get(profile.profile_id)
            if cached is None:
                return None
            created_at, fingerprint, result = cached
            if (
                time.monotonic() - created_at > RESULT_CACHE_TTL_SECONDS
                or not hmac.compare_digest(fingerprint, profile_fingerprint(profile))
            ):
                del self._results[profile.profile_id]
                return None
            return result

    def invalidate(self, profile_id: UUID) -> None:
        with self._lock:
            self._results.pop(profile_id, None)


verification_result_cache = TargetDatabaseVerificationResultCache()


class SchemaSnapshotCollectionError(Exception):
    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category
        self.public_message = message


class ViewDependencyInvestigationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    identity: ServerIdentity
    allowed_privileges: list[str]
    view_names: list[str]
    view_table_usage_available: bool
    view_table_usage_error_code: int | None
    view_table_usage_sqlstate: str | None
    view_table_usage_rows: list[dict[str, str | None]]
    show_create_definitions: dict[str, str]


class TargetDatabaseVerificationService:
    def investigate_view_dependencies(
        self,
        profile: TargetDatabaseProfile,
        password: str,
        *,
        expected_hostname: str,
        expected_engine_version_prefix: str,
        expected_authenticated_user: str,
        expected_effective_user: str,
    ) -> ViewDependencyInvestigationResult:
        if profile.database.casefold() == PROTECTED_REFERENCE_DATABASE.casefold():
            raise SchemaSnapshotCollectionError(
                "REFERENCE_DATABASE_PROTECTED",
                "Database referensi dilindungi; tidak ada koneksi yang dicoba.",
            )
        try:
            connection = pymysql.connect(
                host=profile.host,
                port=profile.port,
                user=profile.username,
                password=password,
                database=profile.database,
                connect_timeout=CONNECT_TIMEOUT_SECONDS,
                read_timeout=CONNECT_TIMEOUT_SECONDS,
                write_timeout=CONNECT_TIMEOUT_SECONDS,
                charset="utf8mb4",
                autocommit=False,
                local_infile=False,
            )
        except (pymysql.MySQLError, OSError, TimeoutError) as exc:
            category, message = _connection_error(exc)
            raise SchemaSnapshotCollectionError(category, message) from exc

        cursor = None
        result: ViewDependencyInvestigationResult | None = None
        collection_error: SchemaSnapshotCollectionError | None = None
        unexpected_error: Exception | None = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT VERSION(), DATABASE(), @@hostname, @@port, "
                "CURRENT_USER(), USER()"
            )
            row = cursor.fetchone()
            if row is None:
                raise SchemaSnapshotCollectionError(
                    "IDENTITY_UNVERIFIED",
                    "Identitas target tidak dapat diverifikasi; investigasi diblokir.",
                )
            identity = ServerIdentity(
                engine_version=str(row[0]),
                database=str(row[1]),
                server_hostname=str(row[2]),
                server_port=int(row[3]),
                effective_user=str(row[4]),
                authenticated_user=str(row[5]),
            )
            if not _identity_matches(profile, identity) or (
                identity.server_hostname.casefold() != expected_hostname.casefold()
                or not identity.engine_version.startswith(expected_engine_version_prefix)
                or identity.authenticated_user.casefold()
                != expected_authenticated_user.casefold()
                or identity.effective_user.casefold()
                != expected_effective_user.casefold()
            ):
                raise SchemaSnapshotCollectionError(
                    "IDENTITY_MISMATCH",
                    "Identitas target tidak cocok; investigasi diblokir.",
                )

            cursor.execute("SHOW GRANTS")
            grants = [str(grant_row[0]) for grant_row in cursor.fetchall()]
            privileges_verified, target_read_only, write_privileges_detected = (
                _assess_grants(grants, profile.database)
            )
            if not privileges_verified:
                raise SchemaSnapshotCollectionError(
                    "PRIVILEGES_UNVERIFIED",
                    "Hak akses tidak dapat diverifikasi; investigasi diblokir.",
                )
            if not target_read_only or write_privileges_detected:
                raise SchemaSnapshotCollectionError(
                    "PRIVILEGES_BLOCKED",
                    "Hak akses melampaui cakupan read-only yang diizinkan.",
                )

            cursor.execute(
                """
                SELECT TABLE_NAME, VIEW_DEFINITION
                FROM INFORMATION_SCHEMA.VIEWS
                WHERE TABLE_SCHEMA = %s
                ORDER BY TABLE_NAME
                """,
                (profile.database,),
            )
            view_rows = cursor.fetchall()
            view_names = [str(view_row[0]) for view_row in view_rows]
            dependency_rows: list[dict[str, str | None]] = []
            dependency_error_code: int | None = None
            dependency_sqlstate: str | None = None
            dependency_available = True
            try:
                cursor.execute(
                    """
                    SELECT VIEW_NAME, TABLE_SCHEMA, TABLE_NAME
                    FROM INFORMATION_SCHEMA.VIEW_TABLE_USAGE
                    WHERE VIEW_SCHEMA = %s
                    ORDER BY VIEW_NAME, TABLE_SCHEMA, TABLE_NAME
                    """,
                    (profile.database,),
                )
                dependency_rows = [
                    {
                        "view_name": str(dependency[0]),
                        "schema_name": (
                            str(dependency[1]) if dependency[1] is not None else None
                        ),
                        "table_name": (
                            str(dependency[2]) if dependency[2] is not None else None
                        ),
                    }
                    for dependency in cursor.fetchall()
                ]
            except pymysql.MySQLError as exc:
                dependency_available = False
                dependency_error_code = (
                    exc.args[0] if exc.args and isinstance(exc.args[0], int) else None
                )
                sqlstate = getattr(exc, "sqlstate", None)
                dependency_sqlstate = str(sqlstate) if sqlstate else None

            show_create_definitions: dict[str, str] = {}
            if not dependency_available:
                database_identifier = profile.database.replace("`", "``")
                for view_name in view_names:
                    view_identifier = view_name.replace("`", "``")
                    cursor.execute(
                        f"SHOW CREATE VIEW `{database_identifier}`.`{view_identifier}`"
                    )
                    create_row = cursor.fetchone()
                    if create_row is None or len(create_row) < 2:
                        raise SchemaSnapshotCollectionError(
                            "SHOW_CREATE_VIEW_FAILED",
                            "Definisi view tidak dapat diperoleh melalui SHOW CREATE VIEW.",
                        )
                    show_create_definitions[view_name] = str(create_row[1])

            result = ViewDependencyInvestigationResult(
                identity=identity,
                allowed_privileges=_target_read_only_privileges(
                    grants,
                    profile.database,
                ),
                view_names=view_names,
                view_table_usage_available=dependency_available,
                view_table_usage_error_code=dependency_error_code,
                view_table_usage_sqlstate=dependency_sqlstate,
                view_table_usage_rows=dependency_rows,
                show_create_definitions=show_create_definitions,
            )
        except SchemaSnapshotCollectionError as exc:
            collection_error = exc
        except (pymysql.MySQLError, OSError, TimeoutError) as exc:
            collection_error = SchemaSnapshotCollectionError(
                "METADATA_INVESTIGATION_FAILED",
                "Metadata dependensi view tidak dapat diinvestigasi.",
            )
            collection_error.__cause__ = exc
        except Exception as exc:
            unexpected_error = exc

        cleanup_failed = False
        if cursor is not None:
            try:
                cursor.close()
            except (pymysql.MySQLError, OSError):
                cleanup_failed = True
        try:
            connection.close()
        except (pymysql.MySQLError, OSError):
            cleanup_failed = True
        if cleanup_failed:
            raise SchemaSnapshotCollectionError(
                "CONNECTION_CLEANUP_FAILED",
                "Koneksi tidak dapat ditutup dengan aman; hasil investigasi ditolak.",
            )
        if collection_error is not None:
            raise collection_error
        if unexpected_error is not None:
            raise unexpected_error
        if result is None:
            raise SchemaSnapshotCollectionError(
                "METADATA_INVESTIGATION_FAILED",
                "Metadata dependensi view tidak dapat diinvestigasi.",
            )
        return result

    def collect_schema_snapshot(
        self,
        profile: TargetDatabaseProfile,
        password: str,
        *,
        expected_hostname: str,
        expected_engine_version_prefix: str,
        expected_authenticated_user: str,
        expected_effective_user: str,
    ) -> TargetSchemaSnapshot:
        if profile.database.casefold() == PROTECTED_REFERENCE_DATABASE.casefold():
            raise SchemaSnapshotCollectionError(
                "REFERENCE_DATABASE_PROTECTED",
                "Database referensi dilindungi; tidak ada koneksi yang dicoba.",
            )
        try:
            connection = pymysql.connect(
                host=profile.host,
                port=profile.port,
                user=profile.username,
                password=password,
                database=profile.database,
                connect_timeout=CONNECT_TIMEOUT_SECONDS,
                read_timeout=CONNECT_TIMEOUT_SECONDS,
                write_timeout=CONNECT_TIMEOUT_SECONDS,
                charset="utf8mb4",
                autocommit=False,
                local_infile=False,
            )
        except (pymysql.MySQLError, OSError, TimeoutError) as exc:
            category, message = _connection_error(exc)
            raise SchemaSnapshotCollectionError(category, message) from exc

        cursor = None
        snapshot: TargetSchemaSnapshot | None = None
        collection_error: SchemaSnapshotCollectionError | None = None
        unexpected_error: Exception | None = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT VERSION(), DATABASE(), @@hostname, @@port, "
                "CURRENT_USER(), USER()"
            )
            row = cursor.fetchone()
            if row is None:
                raise SchemaSnapshotCollectionError(
                    "IDENTITY_UNVERIFIED",
                    "Identitas target tidak dapat diverifikasi; metadata tidak dikumpulkan.",
                )
            identity = ServerIdentity(
                engine_version=str(row[0]),
                database=str(row[1]),
                server_hostname=str(row[2]),
                server_port=int(row[3]),
                effective_user=str(row[4]),
                authenticated_user=str(row[5]),
            )
            if not _identity_matches(profile, identity):
                raise SchemaSnapshotCollectionError(
                    "IDENTITY_MISMATCH",
                    "Identitas target tidak cocok; metadata tidak dikumpulkan.",
                )
            if (
                identity.server_hostname.casefold() != expected_hostname.casefold()
                or not identity.engine_version.startswith(expected_engine_version_prefix)
                or identity.authenticated_user.casefold()
                != expected_authenticated_user.casefold()
                or identity.effective_user.casefold()
                != expected_effective_user.casefold()
            ):
                raise SchemaSnapshotCollectionError(
                    "IDENTITY_MISMATCH",
                    "Hostname, engine, atau account server berbeda dari identitas yang diharapkan.",
                )

            cursor.execute("SHOW GRANTS")
            grants = [str(grant_row[0]) for grant_row in cursor.fetchall()]
            privileges_verified, target_read_only, write_privileges_detected = (
                _assess_grants(grants, profile.database)
            )
            if not privileges_verified:
                raise SchemaSnapshotCollectionError(
                    "PRIVILEGES_UNVERIFIED",
                    "Hak akses tidak dapat diverifikasi; metadata tidak dikumpulkan.",
                )
            if not target_read_only or write_privileges_detected:
                raise SchemaSnapshotCollectionError(
                    "PRIVILEGES_BLOCKED",
                    "Hak akses melampaui cakupan read-only yang diizinkan.",
                )
            allowed_privileges = _target_read_only_privileges(grants, profile.database)
            collected, gaps = collect_schema_metadata(cursor, profile.database)
            captured_at = datetime.now(timezone.utc)
            snapshot = build_target_schema_snapshot(
                profile=profile,
                identity=identity,
                **collected,
                metadata_gaps=gaps,
                captured_at=captured_at.isoformat(),
                allowed_privileges=allowed_privileges,
            )
        except SchemaSnapshotCollectionError as exc:
            collection_error = exc
        except (pymysql.MySQLError, OSError, TimeoutError) as exc:
            collection_error = SchemaSnapshotCollectionError(
                "METADATA_COLLECTION_FAILED",
                "Metadata schema tidak dapat dikumpulkan; tidak ada snapshot yang dibuat.",
            )
            collection_error.__cause__ = exc
        except Exception as exc:
            unexpected_error = exc

        cleanup_failed = False
        if cursor is not None:
            try:
                cursor.close()
            except (pymysql.MySQLError, OSError):
                cleanup_failed = True
        try:
            connection.close()
        except (pymysql.MySQLError, OSError):
            cleanup_failed = True
        if cleanup_failed:
            raise SchemaSnapshotCollectionError(
                "CONNECTION_CLEANUP_FAILED",
                "Koneksi tidak dapat ditutup dengan aman; snapshot tidak dibuat.",
            )
        if collection_error is not None:
            raise collection_error
        if unexpected_error is not None:
            raise unexpected_error
        if snapshot is None:
            raise SchemaSnapshotCollectionError(
                "METADATA_COLLECTION_FAILED",
                "Metadata schema tidak dapat dikumpulkan; tidak ada snapshot yang dibuat.",
            )
        return snapshot

    def verify(
        self,
        profile: TargetDatabaseProfile,
        password: str,
    ) -> TargetDatabaseVerificationResult:
        if profile.database.casefold() == PROTECTED_REFERENCE_DATABASE.casefold():
            return self._result(
                profile,
                status="BLOCKED",
                statuses=["BLOCKED", "PRIVILEGES_UNVERIFIED"],
                message=(
                    "Database referensi dilindungi dan koneksi ditolak sebelum "
                    "percobaan jaringan."
                ),
                error_category="REFERENCE_DATABASE_PROTECTED",
                privileges_status="PRIVILEGES_UNVERIFIED",
            )

        try:
            connection = pymysql.connect(
                host=profile.host,
                port=profile.port,
                user=profile.username,
                password=password,
                database=profile.database,
                connect_timeout=CONNECT_TIMEOUT_SECONDS,
                read_timeout=CONNECT_TIMEOUT_SECONDS,
                write_timeout=CONNECT_TIMEOUT_SECONDS,
                charset="utf8mb4",
                autocommit=False,
                local_infile=False,
            )
        except (pymysql.MySQLError, OSError, TimeoutError) as exc:
            category, message = _connection_error(exc)
            return self._result(
                profile,
                status="CONNECTION_FAILED",
                statuses=["CONNECTION_FAILED", "PRIVILEGES_UNVERIFIED"],
                message=message,
                error_category=category,
                privileges_status="PRIVILEGES_UNVERIFIED",
            )

        cursor = None
        try:
            cursor = connection.cursor()
            result = self._inspect(profile, cursor)
        except (pymysql.MySQLError, OSError, TimeoutError):
            result = self._result(
                profile,
                status="CONNECTION_FAILED",
                statuses=["CONNECTION_FAILED", "PRIVILEGES_UNVERIFIED"],
                message="Koneksi terbuka tetapi identitas server tidak dapat diverifikasi.",
                error_category="IDENTITY_UNVERIFIED",
                privileges_status="PRIVILEGES_UNVERIFIED",
            )

        cleanup_failed = False
        if cursor is not None:
            try:
                cursor.close()
            except (pymysql.MySQLError, OSError):
                cleanup_failed = True
        try:
            connection.close()
        except (pymysql.MySQLError, OSError):
            cleanup_failed = True

        if cleanup_failed:
            return self._result(
                profile,
                status="BLOCKED",
                statuses=["BLOCKED", "CONNECTION_CLEANUP_FAILED"],
                message="Koneksi tidak dapat ditutup dengan aman; hasil tidak diterima.",
                error_category="CONNECTION_CLEANUP_FAILED",
                privileges_status=result.privileges_status,
            )
        return result

    def _inspect(
        self,
        profile: TargetDatabaseProfile,
        cursor: Any,
    ) -> TargetDatabaseVerificationResult:
        cursor.execute(
            "SELECT VERSION(), DATABASE(), @@hostname, @@port, CURRENT_USER(), USER()"
        )
        row = cursor.fetchone()
        if row is None:
            return self._identity_failure(profile, None)

        identity = ServerIdentity(
            engine_version=str(row[0]),
            database=str(row[1]),
            server_hostname=str(row[2]),
            server_port=int(row[3]),
            effective_user=str(row[4]),
            authenticated_user=str(row[5]),
        )
        if not _identity_matches(profile, identity):
            return self._identity_failure(profile, identity)

        try:
            cursor.execute("SHOW GRANTS")
            grants = [str(grant_row[0]) for grant_row in cursor.fetchall()]
        except pymysql.MySQLError:
            return self._result(
                profile,
                status="BLOCKED",
                statuses=[
                    "CONNECTION_SUCCESS",
                    "IDENTITY_VERIFIED",
                    "PRIVILEGES_UNVERIFIED",
                    "BLOCKED",
                ],
                message=(
                    "Identitas terverifikasi, tetapi hak akses tidak dapat "
                    "diverifikasi; pemeriksaan schema diblokir."
                ),
                error_category="PRIVILEGES_UNVERIFIED",
                identity=identity,
                privileges_status="PRIVILEGES_UNVERIFIED",
            )

        privileges_verified, target_read_only, write_privileges_detected = (
            _assess_grants(grants, profile.database)
        )
        if not privileges_verified:
            return self._result(
                profile,
                status="BLOCKED",
                statuses=[
                    "CONNECTION_SUCCESS",
                    "IDENTITY_VERIFIED",
                    "PRIVILEGES_UNVERIFIED",
                    "BLOCKED",
                ],
                message=(
                    "Format atau cakupan hak akses tidak dapat diverifikasi "
                    "secara aman; pemeriksaan schema diblokir."
                ),
                error_category="PRIVILEGES_UNVERIFIED",
                identity=identity,
                privileges_status="PRIVILEGES_UNVERIFIED",
            )
        if not target_read_only:
            return self._result(
                profile,
                status="BLOCKED",
                statuses=[
                    "CONNECTION_SUCCESS",
                    "IDENTITY_VERIFIED",
                    "PRIVILEGES_VERIFIED",
                    "BLOCKED",
                ],
                message=(
                    "Akun tidak memiliki cakupan least-privilege yang disyaratkan "
                    "yaitu SELECT hanya pada database target; pemeriksaan schema "
                    "diblokir."
                ),
                error_category=(
                    "WRITE_PRIVILEGES_DETECTED"
                    if write_privileges_detected
                    else "NON_LEAST_PRIVILEGE_GRANTS"
                ),
                identity=identity,
                privileges_status="PRIVILEGES_VERIFIED",
                write_privileges_detected=write_privileges_detected,
            )

        try:
            schema = _collect_schema_metadata(cursor, profile.database)
        except pymysql.MySQLError:
            return self._result(
                profile,
                status="BLOCKED",
                statuses=[
                    "CONNECTION_SUCCESS",
                    "IDENTITY_VERIFIED",
                    "PRIVILEGES_VERIFIED",
                    "SCHEMA_METADATA_FAILED",
                    "SCHEMA_REVIEW_REQUIRED",
                ],
                message=(
                    "Identitas dan hak akses terverifikasi, tetapi metadata "
                    "schema tidak dapat dikumpulkan."
                ),
                error_category="SCHEMA_METADATA_FAILED",
                identity=identity,
                privileges_status="PRIVILEGES_VERIFIED",
            )

        return self._result(
            profile,
            status="SCHEMA_REVIEW_REQUIRED",
            statuses=[
                "CONNECTION_SUCCESS",
                "IDENTITY_VERIFIED",
                "PRIVILEGES_VERIFIED",
                "SCHEMA_METADATA_COLLECTED",
                "SCHEMA_BASELINE_UNAVAILABLE",
                "SCHEMA_REVIEW_REQUIRED",
            ],
            message=(
                "Metadata berhasil dikumpulkan. Baseline target otoritatif belum "
                "disetujui; hasil ini bukan persetujuan kompatibilitas impor."
            ),
            identity=identity,
            privileges_status="PRIVILEGES_VERIFIED",
            schema_metadata=schema,
        )

    def _identity_failure(
        self,
        profile: TargetDatabaseProfile,
        identity: ServerIdentity | None,
    ) -> TargetDatabaseVerificationResult:
        return self._result(
            profile,
            status="IDENTITY_MISMATCH",
            statuses=["CONNECTION_SUCCESS", "IDENTITY_MISMATCH", "BLOCKED"],
            message=(
                "Identitas server/database tidak cocok dengan profil yang "
                "dikonfirmasi; pemeriksaan schema diblokir."
            ),
            error_category="IDENTITY_MISMATCH",
            identity=identity,
            privileges_status="PRIVILEGES_UNVERIFIED",
        )

    @staticmethod
    def _result(
        profile: TargetDatabaseProfile,
        *,
        status: str,
        statuses: list[str],
        message: str,
        privileges_status: str,
        error_category: str | None = None,
        identity: ServerIdentity | None = None,
        write_privileges_detected: bool = False,
        schema_metadata: SchemaMetadata | None = None,
    ) -> TargetDatabaseVerificationResult:
        return TargetDatabaseVerificationResult(
            profile_id=profile.profile_id,
            profile_fingerprint=profile_fingerprint(profile),
            verified_at=datetime.now(timezone.utc).isoformat(),
            status=status,
            statuses=statuses,
            message=message,
            error_category=error_category,
            identity=identity,
            privileges_status=privileges_status,
            write_privileges_detected=write_privileges_detected,
            schema_metadata=schema_metadata,
        )


def production_confirmation_phrase(profile: TargetDatabaseProfile) -> str:
    return (
        f"CONFIRM PRODUCTION {profile.database} "
        f"ON {profile.host}:{profile.port}"
    )


def _identity_matches(
    profile: TargetDatabaseProfile,
    identity: ServerIdentity,
) -> bool:
    if (
        identity.database != profile.database
        or identity.server_port != profile.port
    ):
        return False
    if (
        identity.authenticated_user.split("@", maxsplit=1)[0] != profile.username
        or identity.effective_user.split("@", maxsplit=1)[0] != profile.username
    ):
        return False
    if (
        identity.database.casefold() == PROTECTED_REFERENCE_DATABASE.casefold()
        and identity.server_hostname.casefold().rstrip(".") == "laptop-h752smp0"
        and identity.server_port == 3306
    ):
        return False
    return True


def _assess_grants(grants: list[str], database: str) -> tuple[bool, bool, bool]:
    if not grants:
        return False, False, False

    expected_scope = f"{database}.*".casefold()
    found_target_select = False
    write_privileges_detected = False
    grants_within_target_scope = True
    known_privileges = {
        "ALTER",
        "ALTER ROUTINE",
        "CREATE",
        "CREATE ROUTINE",
        "CREATE TEMPORARY TABLES",
        "CREATE USER",
        "CREATE VIEW",
        "DELETE",
        "DROP",
        "EVENT",
        "EXECUTE",
        "FILE",
        "INDEX",
        "INSERT",
        "LOCK TABLES",
        "PROCESS",
        "REFERENCES",
        "RELOAD",
        "REPLICATION CLIENT",
        "REPLICATION SLAVE",
        "SELECT",
        "SHOW DATABASES",
        "SHOW VIEW",
        "SHUTDOWN",
        "SUPER",
        "TRIGGER",
        "UPDATE",
        "USAGE",
    }
    write_privileges = {
        "ALTER",
        "ALTER ROUTINE",
        "CREATE",
        "CREATE ROUTINE",
        "CREATE TEMPORARY TABLES",
        "CREATE USER",
        "CREATE VIEW",
        "DELETE",
        "DROP",
        "EVENT",
        "EXECUTE",
        "INDEX",
        "INSERT",
        "LOCK TABLES",
        "REFERENCES",
        "RELOAD",
        "SHUTDOWN",
        "SUPER",
        "TRIGGER",
        "UPDATE",
    }
    for grant in grants:
        match = _GRANT_PATTERN.match(grant.strip())
        if match is None:
            return False, False, write_privileges_detected
        privileges = {
            privilege.strip().upper()
            for privilege in match.group(1).split(",")
        }
        if "ALL" in privileges or "ALL PRIVILEGES" in privileges:
            write_privileges_detected = True
            continue
        if not privileges.issubset(known_privileges):
            return False, False, write_privileges_detected
        if privileges.intersection(write_privileges) or "WITH GRANT OPTION" in grant.upper():
            write_privileges_detected = True
        scope = match.group(2).replace("`", "").casefold()
        if privileges == {"USAGE"} and scope == "*.*":
            continue
        if (
            privileges.issubset({"SELECT", "SHOW VIEW"})
            and privileges
            and scope == expected_scope
        ):
            found_target_select = found_target_select or "SELECT" in privileges
            continue
        grants_within_target_scope = False
    return (
        True,
        found_target_select
        and grants_within_target_scope
        and not write_privileges_detected,
        write_privileges_detected,
    )


def _target_read_only_privileges(grants: list[str], database: str) -> list[str]:
    expected_scope = f"{database}.*".casefold()
    privileges: set[str] = set()
    for grant in grants:
        match = _GRANT_PATTERN.match(grant.strip())
        if match is None:
            continue
        scope = match.group(2).replace("`", "").casefold()
        if scope == expected_scope:
            privileges.update(
                privilege.strip().upper()
                for privilege in match.group(1).split(",")
            )
    return sorted(privileges)


def _collect_schema_metadata(cursor: Any, database: str) -> SchemaMetadata:
    cursor.execute(_TABLES_QUERY, (database,))
    table_rows = cursor.fetchall()
    cursor.execute(_COLUMNS_QUERY, (database,))
    column_rows = cursor.fetchall()
    cursor.execute(_PRIMARY_KEYS_QUERY, (database,))
    primary_key_rows = cursor.fetchall()
    cursor.execute(_FOREIGN_KEYS_QUERY, (database,))
    foreign_key_rows = cursor.fetchall()
    cursor.execute(_UNIQUE_INDEXES_QUERY, (database,))
    unique_index_rows = cursor.fetchall()
    cursor.execute(_AUTO_INCREMENT_QUERY, (database, "%auto_increment%"))
    auto_increment_rows = cursor.fetchall()

    primary_keys: dict[str, list[str]] = {}
    for table, column, _ in primary_key_rows:
        primary_keys.setdefault(str(table), []).append(str(column))

    foreign_keys: dict[tuple[str, str], dict[str, Any]] = {}
    for table, column, constraint, referenced_table, referenced_column, _ in foreign_key_rows:
        key = (str(table), str(constraint))
        definition = foreign_keys.setdefault(
            key,
            {
                "table": str(table),
                "constraint": str(constraint),
                "columns": [],
                "referenced_table": str(referenced_table),
                "referenced_columns": [],
            },
        )
        definition["columns"].append(str(column))
        definition["referenced_columns"].append(str(referenced_column))

    unique_indexes: dict[tuple[str, str], dict[str, Any]] = {}
    for table, index, column, _ in unique_index_rows:
        key = (str(table), str(index))
        definition = unique_indexes.setdefault(
            key,
            {"table": str(table), "index": str(index), "columns": []},
        )
        definition["columns"].append(str(column))

    auto_increment_tables = sorted({str(row[0]) for row in auto_increment_rows})
    return SchemaMetadata(
        base_table_count=sum(str(row[1]).upper() == "BASE TABLE" for row in table_rows),
        view_count=sum(str(row[1]).upper() == "VIEW" for row in table_rows),
        column_count=len(column_rows),
        primary_key_count=len(primary_keys),
        foreign_key_count=len(foreign_keys),
        unique_index_count=len(unique_indexes),
        auto_increment_table_count=len(auto_increment_tables),
        columns=[
            ColumnDefinition(
                table=str(row[0]),
                column=str(row[1]),
                column_type=str(row[2]),
                nullable=str(row[3]).upper() == "YES",
                extra=str(row[4] or ""),
            )
            for row in column_rows
        ],
        primary_keys=[
            PrimaryKeyDefinition(table=table, columns=columns)
            for table, columns in sorted(primary_keys.items())
        ],
        foreign_keys=[
            ForeignKeyDefinition(**definition)
            for _, definition in sorted(foreign_keys.items())
        ],
        unique_indexes=[
            UniqueIndexDefinition(**definition)
            for _, definition in sorted(unique_indexes.items())
        ],
        auto_increment_tables=auto_increment_tables,
    )


def _connection_error(exc: Exception) -> tuple[str, str]:
    if isinstance(exc, TimeoutError):
        return "CONNECTION_TIMEOUT", "Waktu koneksi habis; tidak ada pemeriksaan schema."
    error_code = exc.args[0] if exc.args else None
    if error_code in (1045, 1698):
        return (
            "AUTHENTICATION_FAILED",
            "Autentikasi gagal; periksa username dan password yang dimasukkan.",
        )
    if error_code in (2002, 2003, 2005, 2013, 2055):
        return (
            "NETWORK_ERROR",
            "Endpoint target tidak dapat dijangkau atau koneksi terputus.",
        )
    return "CONNECTION_FAILED", "Koneksi ke target gagal; detail internal disembunyikan."
