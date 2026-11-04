import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Literal
from uuid import UUID, uuid4

import pymysql
from pydantic import BaseModel, ConfigDict, model_validator

from app.config import DATA_DIR
from app.models.target_database import TargetDatabaseProfile

SCHEMA_SNAPSHOT_VERSION = 1
_CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?i)\b(?:password|passwd|secret|token|api[_-]?key|credential)\b"
    r"\s*(?:=|:)\s*(?:'[^']*'|\"[^\"]*\"|[^\s,;]+)"
)


class SnapshotIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    database: str
    environment: str
    host: str
    port: int
    engine_version: str
    server_hostname: str
    server_port: int
    authenticated_user: str
    effective_user: str


class SnapshotVerification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    statuses: list[Literal["IDENTITY_VERIFIED", "PRIVILEGES_VERIFIED"]]
    allowed_privileges: list[str]
    allowed_scope: str


class SnapshotTarget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: UUID
    profile_revision: int
    identity: SnapshotIdentity
    verification: SnapshotVerification


class SnapshotSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_tables: int | None
    views: int | None
    columns_total: int | None
    columns_base_tables: int | None
    columns_views: int | None
    primary_key_constraints: int | None
    primary_key_tables: int | None
    primary_key_columns: int | None
    foreign_key_constraints: int | None
    unique_indexes_excluding_primary: int | None
    unique_constraints: int | None
    auto_increment_tables: int | None


class TableMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    engine: str | None
    table_collation: str | None
    table_comment: str | None
    auto_increment_value: int | None


class ColumnMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    column_name: str
    ordinal_position: int
    data_type: str
    column_type: str
    character_maximum_length: int | None
    numeric_precision: int | None
    numeric_scale: int | None
    nullable: bool
    default_value: str | int | float | None
    extra: str | None
    character_set: str | None
    collation: str | None
    column_comment: str | None


class PrimaryKeyMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    constraint_name: str
    column_name: str
    ordinal_position: int


class ForeignKeyMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    child_table: str
    child_column: str
    parent_table: str
    parent_column: str
    constraint_name: str
    update_rule: str | None
    delete_rule: str | None
    ordinal_position: int


class IndexColumnMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    column_name: str | None
    ordinal_position: int
    cardinality: int | None


class IndexMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    index_name: str
    unique: bool
    index_type: str
    columns: list[IndexColumnMetadata]


class ViewDependency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_name: str | None
    table_name: str | None


def extract_view_dependencies(
    definition: str,
    default_schema: str,
) -> list[ViewDependency]:
    tokens = _view_definition_tokens(definition)
    dependencies: dict[tuple[str, str], ViewDependency] = {}
    for index, token in enumerate(tokens):
        if token[0] != "WORD" or token[1].upper() not in {"FROM", "JOIN"}:
            continue
        cursor = index + 1
        while cursor < len(tokens) and tokens[cursor][0] == "(":
            cursor += 1
        while (
            cursor < len(tokens)
            and tokens[cursor][0] == "WORD"
            and tokens[cursor][1].upper() in {"LATERAL", "ONLY"}
        ):
            cursor += 1
        if cursor >= len(tokens) or (
            tokens[cursor][0] == "WORD"
            and tokens[cursor][1].upper() in {"SELECT", "WITH"}
        ):
            continue
        if tokens[cursor][0] not in {"IDENTIFIER", "WORD"}:
            continue
        first_name = tokens[cursor][1]
        schema_name = default_schema
        table_name = first_name
        next_cursor = cursor + 1
        if (
            next_cursor + 1 < len(tokens)
            and tokens[next_cursor][0] == "."
            and tokens[next_cursor + 1][0] in {"IDENTIFIER", "WORD"}
        ):
            schema_name = first_name
            table_name = tokens[next_cursor + 1][1]
        key = (schema_name.casefold(), table_name.casefold())
        dependencies[key] = ViewDependency(
            schema_name=schema_name,
            table_name=table_name,
        )
    return sorted(
        dependencies.values(),
        key=lambda item: (
            (item.schema_name or "").casefold(),
            (item.table_name or "").casefold(),
        ),
    )


def _view_definition_tokens(definition: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    index = 0
    while index < len(definition):
        character = definition[index]
        if character.isspace():
            index += 1
            continue
        if definition.startswith("--", index):
            newline = definition.find("\n", index + 2)
            index = len(definition) if newline < 0 else newline + 1
            continue
        if character == "#":
            newline = definition.find("\n", index + 1)
            index = len(definition) if newline < 0 else newline + 1
            continue
        if definition.startswith("/*", index):
            close = definition.find("*/", index + 2)
            if close < 0:
                raise ValueError("Definisi view memiliki komentar yang tidak tertutup.")
            index = close + 2
            continue
        if character in {"'", '"'}:
            quote = character
            index += 1
            while index < len(definition):
                if definition[index] == "\\":
                    index += 2
                    continue
                if definition[index] == quote:
                    if index + 1 < len(definition) and definition[index + 1] == quote:
                        index += 2
                        continue
                    index += 1
                    break
                index += 1
            else:
                raise ValueError("Definisi view memiliki string yang tidak tertutup.")
            continue
        if character == "`":
            index += 1
            identifier: list[str] = []
            while index < len(definition):
                if definition[index] == "`":
                    if index + 1 < len(definition) and definition[index + 1] == "`":
                        identifier.append("`")
                        index += 2
                        continue
                    index += 1
                    break
                identifier.append(definition[index])
                index += 1
            else:
                raise ValueError(
                    "Definisi view memiliki identifier yang tidak tertutup."
                )
            tokens.append(("IDENTIFIER", "".join(identifier)))
            continue
        if character.isalnum() or character in "_$":
            start = index
            index += 1
            while index < len(definition) and (
                definition[index].isalnum() or definition[index] in "_$"
            ):
                index += 1
            tokens.append(("WORD", definition[start:index]))
            continue
        tokens.append((character, character))
        index += 1
    return tokens


class ViewMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    view_name: str
    definer: str | None
    security_type: str | None
    check_option: str | None
    definition: str | None
    dependencies: list[ViewDependency]


class AutoIncrementMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    column_name: str
    next_value: int | None


class MetadataGap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    component: str
    reason: str


class TargetSchemaSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1]
    snapshot_id: UUID
    captured_at: str
    collection_status: Literal["COMPLETE", "PARTIAL"]
    target: SnapshotTarget
    summary: SnapshotSummary
    tables: list[TableMetadata]
    columns: list[ColumnMetadata]
    primary_keys: list[PrimaryKeyMetadata]
    foreign_keys: list[ForeignKeyMetadata]
    indexes: list[IndexMetadata]
    views: list[ViewMetadata]
    auto_increment: list[AutoIncrementMetadata]
    metadata_gaps: list[MetadataGap]

    @model_validator(mode="after")
    def validate_summary_counts(self) -> "TargetSchemaSnapshot":
        if self.collection_status != "COMPLETE":
            return self
        expected = {
            "base_tables": len(self.tables),
            "views": len(self.views),
            "columns_total": len(self.columns),
            "primary_key_constraints": len(
                {(item.table_name, item.constraint_name) for item in self.primary_keys}
            ),
            "primary_key_tables": len({item.table_name for item in self.primary_keys}),
            "primary_key_columns": len(self.primary_keys),
            "foreign_key_constraints": len(
                {(item.child_table, item.constraint_name) for item in self.foreign_keys}
            ),
            "unique_indexes_excluding_primary": sum(
                item.unique and item.index_name != "PRIMARY" for item in self.indexes
            ),
            "auto_increment_tables": len({item.table_name for item in self.auto_increment}),
        }
        for field, value in expected.items():
            if getattr(self.summary, field) != value:
                raise ValueError(f"Ringkasan snapshot tidak cocok untuk {field}.")
        if self.summary.columns_base_tables + self.summary.columns_views != len(self.columns):
            raise ValueError("Distribusi kolom snapshot tidak cocok.")
        if self.summary.unique_constraints is None:
            raise ValueError("Jumlah unique constraints wajib tersedia pada snapshot lengkap.")
        if self.metadata_gaps:
            raise ValueError("Snapshot lengkap tidak boleh memiliki metadata gap.")
        return self


class SchemaSnapshotStorageError(Exception):
    """Raised when a schema snapshot cannot be safely persisted."""


class SchemaSnapshotStorage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR
        self.snapshot_root = self.data_dir / "schema-snapshots"

    def save(
        self,
        snapshot: TargetSchemaSnapshot,
        *,
        timestamp: str,
    ) -> tuple[Path, str]:
        directory = self.snapshot_root / snapshot.target.identity.database
        self._validate_path(create=True, directory=directory)
        safe_timestamp = re.sub(r"[^0-9-]", "", timestamp)
        if not re.fullmatch(r"\d{8}-\d{6}", safe_timestamp):
            raise SchemaSnapshotStorageError("Timestamp snapshot tidak valid.")
        snapshot_path = directory / f"schema-snapshot-{safe_timestamp}.json"
        checksum_path = snapshot_path.with_suffix(".json.sha256")
        if snapshot_path.exists() or checksum_path.exists():
            raise SchemaSnapshotStorageError(
                "Nama snapshot sudah digunakan; tidak ada file yang ditimpa."
            )

        payload = (
            json.dumps(
                snapshot.model_dump(mode="json"),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        if _CREDENTIAL_ASSIGNMENT.search(payload.decode("utf-8")):
            raise SchemaSnapshotStorageError(
                "Metadata schema mengandung pola credential; snapshot tidak disimpan."
            )
        digest = hashlib.sha256(payload).hexdigest()
        checksum_payload = f"{digest}  {snapshot_path.name}\n".encode("ascii")
        json_temp: Path | None = None
        checksum_temp: Path | None = None
        snapshot_created = False
        try:
            json_temp = self._write_temporary(directory, payload, ".json")
            checksum_temp = self._write_temporary(directory, checksum_payload, ".sha256")
            TargetSchemaSnapshot.model_validate_json(payload)
            os.replace(json_temp, snapshot_path)
            json_temp = None
            snapshot_created = True
            os.replace(checksum_temp, checksum_path)
            checksum_temp = None
        except (OSError, ValueError) as exc:
            if snapshot_created:
                snapshot_path.unlink(missing_ok=True)
            raise SchemaSnapshotStorageError(
                "Snapshot metadata tidak dapat disimpan atau divalidasi."
            ) from exc
        finally:
            if json_temp is not None:
                json_temp.unlink(missing_ok=True)
            if checksum_temp is not None:
                checksum_temp.unlink(missing_ok=True)
        return snapshot_path, digest

    def _validate_path(self, *, create: bool, directory: Path) -> None:
        paths = (self.data_dir, self.snapshot_root, directory)
        if any(path.is_symlink() for path in paths):
            raise SchemaSnapshotStorageError(
                "Path snapshot tidak boleh menggunakan symlink."
            )
        if create:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise SchemaSnapshotStorageError(
                    "Direktori snapshot lokal tidak dapat disiapkan."
                ) from exc
        if not self.data_dir.is_dir() or not self.snapshot_root.is_dir() or not directory.is_dir():
            raise SchemaSnapshotStorageError("Direktori snapshot lokal tidak valid.")

    @staticmethod
    def _write_temporary(directory: Path, payload: bytes, suffix: str) -> Path:
        descriptor, name = tempfile.mkstemp(
            prefix=".schema-snapshot-",
            suffix=suffix,
            dir=directory,
        )
        path = Path(name)
        try:
            with os.fdopen(descriptor, "wb") as target:
                target.write(payload)
                target.flush()
                os.fsync(target.fileno())
        except OSError:
            path.unlink(missing_ok=True)
            raise
        return path


def build_target_schema_snapshot(
    *,
    profile: TargetDatabaseProfile,
    identity: Any,
    tables: list[dict[str, Any]] | None,
    columns: list[dict[str, Any]] | None,
    primary_keys: list[dict[str, Any]] | None,
    foreign_keys: list[dict[str, Any]] | None,
    indexes: list[dict[str, Any]] | None,
    views: list[dict[str, Any]] | None,
    unique_constraints: int | None,
    metadata_gaps: list[MetadataGap],
    captured_at: str,
    allowed_privileges: list[str],
) -> TargetSchemaSnapshot:
    table_records = [TableMetadata.model_validate(item) for item in tables or []]
    column_records = [ColumnMetadata.model_validate(item) for item in columns or []]
    pk_records = [PrimaryKeyMetadata.model_validate(item) for item in primary_keys or []]
    fk_records = [ForeignKeyMetadata.model_validate(item) for item in foreign_keys or []]
    index_records = [IndexMetadata.model_validate(item) for item in indexes or []]
    view_records = [ViewMetadata.model_validate(item) for item in views or []]
    auto_increment = [
        AutoIncrementMetadata(
            table_name=column.table_name,
            column_name=column.column_name,
            next_value=next(
                (
                    table.auto_increment_value
                    for table in table_records
                    if table.table_name == column.table_name
                ),
                None,
            ),
        )
        for column in column_records
        if column.extra and "auto_increment" in column.extra.casefold()
    ]
    base_tables_count = len(table_records) if tables is not None else None
    views_count = len(view_records) if views is not None else None
    columns_count = len(column_records) if columns is not None else None
    columns_base = (
        sum(
            1
            for column in column_records
            if any(table.table_name == column.table_name for table in table_records)
        )
        if tables is not None and columns is not None
        else None
    )
    columns_views = (
        columns_count - columns_base
        if columns_count is not None and columns_base is not None
        else None
    )
    pk_constraints = (
        len({(item.table_name, item.constraint_name) for item in pk_records})
        if primary_keys is not None
        else None
    )
    pk_tables = (
        len({item.table_name for item in pk_records})
        if primary_keys is not None
        else None
    )
    fk_constraints = (
        len({(item.child_table, item.constraint_name) for item in fk_records})
        if foreign_keys is not None
        else None
    )
    unique_index_count = (
        sum(item.unique and item.index_name != "PRIMARY" for item in index_records)
        if indexes is not None
        else None
    )
    auto_increment_table_count = (
        len({item.table_name for item in auto_increment})
        if columns is not None
        else None
    )
    summary = SnapshotSummary(
        base_tables=base_tables_count,
        views=views_count,
        columns_total=columns_count,
        columns_base_tables=columns_base,
        columns_views=columns_views,
        primary_key_constraints=pk_constraints,
        primary_key_tables=pk_tables,
        primary_key_columns=len(pk_records) if primary_keys is not None else None,
        foreign_key_constraints=fk_constraints,
        unique_indexes_excluding_primary=unique_index_count,
        unique_constraints=unique_constraints,
        auto_increment_tables=auto_increment_table_count,
    )
    gaps = list(metadata_gaps)
    if unique_constraints is None and not any(gap.component == "unique_constraints" for gap in gaps):
        gaps.append(
            MetadataGap(
                component="unique_constraints",
                reason="Metadata TABLE_CONSTRAINTS tidak tersedia.",
            )
        )
    return TargetSchemaSnapshot(
        schema_version=SCHEMA_SNAPSHOT_VERSION,
        snapshot_id=uuid4(),
        captured_at=captured_at,
        collection_status="PARTIAL" if gaps else "COMPLETE",
        target=SnapshotTarget(
            profile_id=profile.profile_id,
            profile_revision=profile.revision,
            identity=SnapshotIdentity(
                database=identity.database,
                environment=profile.environment.value,
                host=profile.host,
                port=profile.port,
                engine_version=identity.engine_version,
                server_hostname=identity.server_hostname,
                server_port=identity.server_port,
                authenticated_user=identity.authenticated_user,
                effective_user=identity.effective_user,
            ),
            verification=SnapshotVerification(
                statuses=["IDENTITY_VERIFIED", "PRIVILEGES_VERIFIED"],
                allowed_privileges=sorted(set(allowed_privileges)),
                allowed_scope=f"{profile.database}.*",
            ),
        ),
        summary=summary,
        tables=table_records,
        columns=column_records,
        primary_keys=pk_records,
        foreign_keys=fk_records,
        indexes=index_records,
        views=view_records,
        auto_increment=auto_increment,
        metadata_gaps=gaps,
    )


_METADATA_QUERIES: dict[str, str] = {
    "tables": """
        SELECT TABLE_NAME, ENGINE, TABLE_COLLATION, TABLE_COMMENT, AUTO_INCREMENT
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """,
    "columns": """
        SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, COLUMN_TYPE,
               CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE,
               IS_NULLABLE, COLUMN_DEFAULT, EXTRA, CHARACTER_SET_NAME,
               COLLATION_NAME, COLUMN_COMMENT, TABLE_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        JOIN INFORMATION_SCHEMA.TABLES USING (TABLE_SCHEMA, TABLE_NAME)
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """,
    "primary_keys": """
        SELECT TABLE_NAME, CONSTRAINT_NAME, COLUMN_NAME, ORDINAL_POSITION
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND CONSTRAINT_NAME = 'PRIMARY'
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """,
    "foreign_keys": """
        SELECT k.TABLE_NAME, k.COLUMN_NAME, k.REFERENCED_TABLE_NAME,
               k.REFERENCED_COLUMN_NAME, k.CONSTRAINT_NAME, r.UPDATE_RULE,
               r.DELETE_RULE, k.ORDINAL_POSITION
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS k
        LEFT JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS r
          ON r.CONSTRAINT_SCHEMA = k.CONSTRAINT_SCHEMA
         AND r.TABLE_NAME = k.TABLE_NAME
         AND r.CONSTRAINT_NAME = k.CONSTRAINT_NAME
        WHERE k.TABLE_SCHEMA = %s
          AND k.REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY k.TABLE_NAME, k.CONSTRAINT_NAME, k.ORDINAL_POSITION
    """,
    "indexes": """
        SELECT TABLE_NAME, INDEX_NAME, NON_UNIQUE, INDEX_TYPE, COLUMN_NAME,
               SEQ_IN_INDEX, CARDINALITY
        FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX
    """,
    "unique_constraints": """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
        WHERE CONSTRAINT_SCHEMA = %s AND CONSTRAINT_TYPE = 'UNIQUE'
    """,
    "views": """
        SELECT TABLE_NAME, DEFINER, SECURITY_TYPE, CHECK_OPTION, VIEW_DEFINITION
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
    """,
}


def collect_schema_metadata(
    cursor: Any,
    database: str,
) -> tuple[dict[str, Any], list[MetadataGap]]:
    collected: dict[str, Any] = {}
    gaps: list[MetadataGap] = []
    for component, query in _METADATA_QUERIES.items():
        try:
            cursor.execute(query, (database,))
            rows = cursor.fetchall()
            collected[component] = rows[0][0] if component == "unique_constraints" else rows
        except pymysql.MySQLError:
            collected[component] = None
            gaps.append(
                MetadataGap(
                    component=component,
                    reason=(
                        f"Metadata {component} tidak berhasil dibaca dari "
                        "INFORMATION_SCHEMA."
                    ),
                )
            )

    tables = [
        {
            "table_name": row[0],
            "engine": row[1],
            "table_collation": row[2],
            "table_comment": row[3],
            "auto_increment_value": row[4],
        }
        for row in collected.get("tables") or []
    ]
    columns = [
        {
            "table_name": row[0],
            "column_name": row[1],
            "ordinal_position": row[2],
            "data_type": row[3],
            "column_type": row[4],
            "character_maximum_length": row[5],
            "numeric_precision": row[6],
            "numeric_scale": row[7],
            "nullable": str(row[8]).upper() == "YES",
            "default_value": row[9],
            "extra": row[10],
            "character_set": row[11],
            "collation": row[12],
            "column_comment": row[13],
            "table_type": row[14],
        }
        for row in collected.get("columns") or []
    ]
    column_records = [
        {key: value for key, value in item.items() if key != "table_type"}
        for item in columns
    ]
    primary_keys = [
        {
            "table_name": row[0],
            "constraint_name": row[1],
            "column_name": row[2],
            "ordinal_position": row[3],
        }
        for row in collected.get("primary_keys") or []
    ]
    foreign_keys = [
        {
            "child_table": row[0],
            "child_column": row[1],
            "parent_table": row[2],
            "parent_column": row[3],
            "constraint_name": row[4],
            "update_rule": row[5],
            "delete_rule": row[6],
            "ordinal_position": row[7],
        }
        for row in collected.get("foreign_keys") or []
    ]
    index_groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in collected.get("indexes") or []:
        key = (str(row[0]), str(row[1]))
        group = index_groups.setdefault(
            key,
            {
                "table_name": row[0],
                "index_name": row[1],
                "unique": not bool(row[2]),
                "index_type": row[3],
                "columns": [],
            },
        )
        group["columns"].append(
            {
                "column_name": row[4],
                "ordinal_position": row[5],
                "cardinality": row[6],
            }
        )
    views = None
    if collected.get("views") is not None:
        views = []
        for row in collected["views"]:
            definition = row[4]
            if definition is not None and _CREDENTIAL_ASSIGNMENT.search(str(definition)):
                definition = None
                gaps.append(
                    MetadataGap(
                        component="view_definition",
                        reason=(
                            "Definisi view dengan pola credential tidak disertakan."
                        ),
                    )
                )
            view_name = str(row[0])
            dependencies: list[ViewDependency] = []
            if definition is not None:
                try:
                    dependencies = extract_view_dependencies(
                        str(definition),
                        database,
                    )
                except ValueError:
                    gaps.append(
                        MetadataGap(
                            component=f"view_dependencies:{view_name}",
                            reason=(
                                "Referensi objek pada definisi view tidak dapat "
                                "diparse dengan aman."
                            ),
                        )
                    )
            views.append(
                {
                    "view_name": view_name,
                    "definer": row[1],
                    "security_type": row[2],
                    "check_option": row[3],
                    "definition": definition,
                    "dependencies": dependencies,
                }
            )
    return (
        {
            "tables": tables if collected.get("tables") is not None else None,
            "columns": column_records if collected.get("columns") is not None else None,
            "primary_keys": (
                primary_keys if collected.get("primary_keys") is not None else None
            ),
            "foreign_keys": (
                foreign_keys if collected.get("foreign_keys") is not None else None
            ),
            "indexes": (
                list(index_groups.values())
                if collected.get("indexes") is not None
                else None
            ),
            "views": views,
            "unique_constraints": collected.get("unique_constraints"),
        },
        gaps,
    )
