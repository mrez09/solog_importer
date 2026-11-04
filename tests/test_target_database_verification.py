import re
from pathlib import Path
from uuid import uuid4

import pymysql
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.target_database import (
    TargetDatabaseProfile,
    TargetEnvironment,
)
from app.services.target_database_storage import TargetDatabaseStorage
import app.routers.target_database_verification as verification_router
import app.services.target_database_storage as target_storage_module
import app.services.target_database_verification as verification_module


@pytest.fixture
def target_data_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    monkeypatch.setattr(target_storage_module, "DATA_DIR", data_dir)
    return data_dir


@pytest.fixture
def client() -> TestClient:
    return TestClient(app, base_url="http://localhost")


def build_profile(**overrides: object) -> TargetDatabaseProfile:
    values: dict[str, object] = {
        "profile_id": uuid4(),
        "name": "Synthetic target",
        "environment": TargetEnvironment.STAGING,
        "host": "db-target.test",
        "port": 3307,
        "database": "solog_import_stage",
        "username": "importer_test",
        "purpose": "TARGET",
    }
    values.update(overrides)
    return TargetDatabaseProfile.model_validate(values)


def selected_profile(data_dir: Path, **overrides: object) -> TargetDatabaseProfile:
    profile = build_profile(**overrides)
    storage = TargetDatabaseStorage(data_dir)
    storage.create(profile)
    storage.select(profile.profile_id)
    return profile


def verification_form(
    client: TestClient,
    profile: TargetDatabaseProfile,
    *,
    password: str = "synthetic-password-never-return",
    **overrides: str,
):
    page = client.get("/target-databases/verify")
    token = re.search(
        r'name="verification_token" value="([^"]+)"',
        page.text,
    )
    assert token is not None
    data = {
        "password": password,
        "confirm_target": "yes",
        "verification_token": token.group(1),
    }
    data.update(overrides)
    csrf_token = client.cookies.get("solog_csrf", "")
    return client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data={**data, "csrf_token": csrf_token},
        headers={"Origin": "http://localhost"},
        follow_redirects=False,
    )


class StubVerificationService:
    def __init__(self) -> None:
        self.calls: list[tuple[TargetDatabaseProfile, str]] = []

    def verify(
        self,
        profile: TargetDatabaseProfile,
        password: str,
    ):
        self.calls.append((profile, password))
        return verification_module.TargetDatabaseVerificationResult(
            profile_id=profile.profile_id,
            profile_fingerprint=verification_module.profile_fingerprint(profile),
            verified_at="2026-11-04T00:00:00+00:00",
            status="SCHEMA_REVIEW_REQUIRED",
            statuses=[
                "CONNECTION_SUCCESS",
                "IDENTITY_VERIFIED",
                "PRIVILEGES_VERIFIED",
                "SCHEMA_METADATA_COLLECTED",
                "SCHEMA_BASELINE_UNAVAILABLE",
                "SCHEMA_REVIEW_REQUIRED",
            ],
            message="Synthetic result; baseline remains unavailable.",
            privileges_status="PRIVILEGES_VERIFIED",
        )


class FakeCursor:
    def __init__(
        self,
        *,
        identity: tuple[object, ...] | None = None,
        grants: list[str] | None = None,
        grants_error: Exception | None = None,
    ) -> None:
        self.identity = identity or (
            "10.11.6-MariaDB",
            "solog_import_stage",
            "target-server",
            3307,
            "importer_test@%",
            "importer_test@localhost",
        )
        self.grants = grants or [
            "GRANT USAGE ON *.* TO `importer_test`@`%`",
            "GRANT SELECT ON `solog_import_stage`.* TO `importer_test`@`%`",
        ]
        self.grants_error = grants_error
        self.executed: list[tuple[str, tuple[object, ...] | None]] = []
        self._rows: list[tuple[object, ...]] = []
        self.closed = False

    def execute(
        self,
        query: str,
        params: tuple[object, ...] | None = None,
    ) -> None:
        self.executed.append((query, params))
        if query.startswith("SELECT VERSION()"):
            self._rows = [self.identity]
        elif query == "SHOW GRANTS":
            if self.grants_error:
                raise self.grants_error
            self._rows = [(grant,) for grant in self.grants]
        elif "INFORMATION_SCHEMA.TABLES" in query:
            self._rows = [
                ("headers", "BASE TABLE"),
                ("receipt_view", "VIEW"),
            ]
        elif "INFORMATION_SCHEMA.COLUMNS" in query and "EXTRA LIKE" not in query:
            self._rows = [
                ("headers", "id", "int(11)", "NO", "auto_increment"),
                ("headers", "number", "varchar(40)", "NO", ""),
                ("receipt_view", "label", "varchar(40)", "YES", ""),
            ]
        elif "CONSTRAINT_NAME = 'PRIMARY'" in query:
            self._rows = [("headers", "id", 1)]
        elif "REFERENCED_TABLE_NAME IS NOT NULL" in query:
            self._rows = [
                ("headers", "warehouse_id", "fk_headers_warehouse", "warehouses", "id", 1)
            ]
        elif "INFORMATION_SCHEMA.STATISTICS" in query:
            self._rows = [("headers", "uq_headers_number", "number", 1)]
        elif "EXTRA LIKE" in query:
            self._rows = [("headers",)]
        else:
            raise AssertionError(f"Unexpected query: {query}")

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def fetchall(self):
        return list(self._rows)

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self.fake_cursor = cursor
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.fake_cursor

    def close(self) -> None:
        self.closed = True


def test_no_profile_is_selected_and_no_connection_form_is_shown(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    response = client.get("/target-databases/verify")

    assert response.status_code == 200
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []
    assert "Belum ada target terpilih" in response.text
    assert "Verifikasi identitas &amp; schema" not in response.text
    assert "koneksi belum dicoba" in response.text


def test_verification_requires_explicit_target_selection(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    TargetDatabaseStorage(target_data_dir).create(profile)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)

    response = client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data={
            "password": "synthetic",
            "confirm_target": "yes",
            "csrf_token": client.get("/target-databases").cookies.get(
                "solog_csrf", ""
            ),
        },
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 409
    assert "bukan target yang sedang dipilih" in response.text
    assert stub.calls == []


def test_invalid_or_deleted_profile_cannot_be_verified(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(target_data_dir)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)
    client.get("/target-databases/verify")
    TargetDatabaseStorage(target_data_dir).delete(profile.profile_id)

    response = client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data={
            "password": "synthetic",
            "confirm_target": "yes",
            "csrf_token": client.cookies.get("solog_csrf", ""),
        },
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 404
    assert stub.calls == []
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


def test_profile_change_after_display_invalidates_form_token(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(target_data_dir)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)
    page = client.get("/target-databases/verify")
    token = re.search(r'name="verification_token" value="([^"]+)"', page.text)
    assert token is not None

    storage = TargetDatabaseStorage(target_data_dir)
    storage.update(profile.model_copy(update={"host": "changed-target.test"}))
    response = client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data={
            "password": "synthetic",
            "confirm_target": "yes",
            "verification_token": token.group(1),
            "csrf_token": client.cookies.get("solog_csrf", ""),
        },
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 409
    assert "profil berubah" in response.text
    assert stub.calls == []


@pytest.mark.parametrize(
    (
        "environment",
        "password",
        "confirmation",
        "expected_status",
        "expected_message",
    ),
    [
        (
            TargetEnvironment.DEVELOPMENT,
            "",
            "yes",
            422,
            "Password database wajib",
        ),
        (
            TargetEnvironment.STAGING,
            "",
            "yes",
            422,
            "Password database wajib",
        ),
        (
            TargetEnvironment.PRODUCTION,
            "",
            "yes",
            422,
            "Password database wajib",
        ),
        (
            TargetEnvironment.OTHER,
            "",
            "yes",
            422,
            "Password database wajib",
        ),
        (
            TargetEnvironment.STAGING,
            "synthetic",
            "",
            422,
            "Konfirmasi eksplisit",
        ),
    ],
)
def test_missing_password_or_confirmation_is_rejected(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    environment: TargetEnvironment,
    password: str,
    confirmation: str,
    expected_status: int,
    expected_message: str,
) -> None:
    profile = selected_profile(target_data_dir, environment=environment)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)
    verification_page = client.get("/target-databases/verify")

    response = verification_form(
        client,
        profile,
        password=password,
        confirm_target=confirmation,
    )

    assert response.status_code == expected_status
    assert expected_message in response.text
    assert 'name="password" type="password" required' in verification_page.text
    assert stub.calls == []
    assert "synthetic-password-never-return" not in response.text


def test_production_requires_exact_additional_identity_confirmation(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(
        target_data_dir,
        environment=TargetEnvironment.PRODUCTION,
    )
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)

    response = verification_form(client, profile, production_confirmation="wrong")

    assert response.status_code == 422
    assert "Target Production memerlukan" in response.text
    assert stub.calls == []
    assert "CONFIRM PRODUCTION solog_import_stage ON db-target.test:3307" in client.get(
        "/target-databases/verify"
    ).text


def test_success_response_shows_identity_without_echoing_password(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(target_data_dir)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)

    response = verification_form(client, profile)

    assert response.status_code == 200
    assert "db-target.test" in response.text
    assert "Synthetic result" in response.text
    assert "synthetic-password-never-return" not in response.text
    assert stub.calls == [(profile, "synthetic-password-never-return")]
    persisted = TargetDatabaseStorage(target_data_dir).configuration_path.read_text(
        encoding="utf-8"
    )
    assert "synthetic-password-never-return" not in persisted


@pytest.mark.parametrize("password", ["", "synthetic-local-password"])
def test_local_profile_accepts_empty_or_filled_password(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    password: str,
) -> None:
    profile = selected_profile(
        target_data_dir,
        environment=TargetEnvironment.LOCAL,
    )
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)

    page = client.get("/target-databases/verify")
    assert 'type="password" required' not in page.text
    response = verification_form(client, profile, password=password)

    assert response.status_code == 200
    assert stub.calls == [(profile, password)]
    persisted = TargetDatabaseStorage(target_data_dir).configuration_path.read_text(
        encoding="utf-8"
    )
    if password:
        assert password not in response.text
        assert password not in persisted
    assert "password" not in persisted.casefold()


@pytest.mark.parametrize("password", ["", "synthetic-local-password"])
def test_local_password_is_forwarded_explicitly_to_connector(
    monkeypatch: pytest.MonkeyPatch,
    password: str,
) -> None:
    profile = build_profile(environment=TargetEnvironment.LOCAL)
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    connect_options: dict[str, object] = {}

    def connector(**kwargs: object) -> FakeConnection:
        connect_options.update(kwargs)
        return connection

    monkeypatch.setattr(verification_module.pymysql, "connect", connector)
    verification_module.TargetDatabaseVerificationService().verify(profile, password)

    assert "password" in connect_options
    assert connect_options["password"] == password
    assert connection.closed is True
    assert cursor.closed is True


def test_snapshot_export_is_rejected_for_other_profiles_before_connection(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(target_data_dir)

    class ForbiddenSnapshotService(StubVerificationService):
        def collect_schema_snapshot(self, *args: object, **kwargs: object) -> None:
            _ = args, kwargs
            raise AssertionError("Snapshot export must not connect for this profile.")

    stub = ForbiddenSnapshotService()
    monkeypatch.setattr(verification_router, "verification_service", stub)

    response = verification_form(
        client,
        profile,
        action="export_schema_snapshot",
    )

    assert response.status_code == 422
    assert "Ekspor snapshot hanya tersedia" in response.text
    assert stub.calls == []


def test_profile_update_invalidates_cached_verification(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    profile = selected_profile(target_data_dir)
    result = StubVerificationService().verify(profile, "transient-password")
    verification_module.verification_result_cache.put(profile, result)

    response = client.post(
        f"/target-databases/{profile.profile_id}/update",
        data={
            "name": "Edited target",
            "environment": "Staging",
            "host": "changed-target.test",
            "port": "3307",
            "database": "solog_import_stage",
            "username": "importer_test",
            "password": "",
            "csrf_token": client.get("/target-databases").cookies.get(
                "solog_csrf", ""
            ),
        },
        headers={"Origin": "http://localhost"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert (
        TargetDatabaseStorage(target_data_dir).load().selected_profile_id
        == profile.profile_id
    )
    page = client.get("/target-databases/verify")
    assert "Synthetic result" not in page.text
    assert verification_module.verification_result_cache.get(
        TargetDatabaseStorage(target_data_dir).load().profiles[0]
    ) is None


def test_reference_database_is_rejected_before_connector_is_called(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile(
        host="other-host.test",
        database="DB_SOLOG_OLI_INITIAL",
        port=3306,
    )
    connector_called = False

    def forbidden_connector(**kwargs: object) -> None:
        nonlocal connector_called
        _ = kwargs
        connector_called = True

    monkeypatch.setattr(verification_module.pymysql, "connect", forbidden_connector)
    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "BLOCKED"
    assert result.error_category == "REFERENCE_DATABASE_PROTECTED"
    assert connector_called is False


@pytest.mark.parametrize(
    ("exception", "category"),
    [
        (TimeoutError("synthetic password should not appear"), "CONNECTION_TIMEOUT"),
        (
            pymysql.err.OperationalError(1045, "synthetic authentication failure"),
            "AUTHENTICATION_FAILED",
        ),
    ],
)
def test_connection_failure_is_sanitized_and_does_not_log_password(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    exception: Exception,
    category: str,
) -> None:
    profile = build_profile()

    def failed_connector(**kwargs: object) -> None:
        _ = kwargs
        raise exception

    monkeypatch.setattr(verification_module.pymysql, "connect", failed_connector)
    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "CONNECTION_FAILED"
    assert result.error_category == category
    assert "synthetic password" not in result.message
    assert "synthetic authentication failure" not in result.message
    assert "synthetic-password" not in caplog.text


def test_successful_schema_verification_uses_only_metadata_queries_and_closes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    connect_options: dict[str, object] = {}

    def connector(**kwargs: object) -> FakeConnection:
        connect_options.update(kwargs)
        return connection

    monkeypatch.setattr(verification_module.pymysql, "connect", connector)
    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "SCHEMA_REVIEW_REQUIRED"
    assert "SCHEMA_BASELINE_UNAVAILABLE" in result.statuses
    assert result.schema_metadata is not None
    assert result.schema_metadata.base_table_count == 1
    assert result.schema_metadata.view_count == 1
    assert result.schema_metadata.column_count == 3
    assert result.schema_metadata.primary_keys[0].columns == ["id"]
    assert result.schema_metadata.foreign_keys[0].referenced_table == "warehouses"
    assert result.schema_metadata.unique_indexes[0].index == "uq_headers_number"
    assert result.schema_metadata.auto_increment_tables == ["headers"]
    assert connection.closed is True
    assert cursor.closed is True
    assert connect_options["password"] == "synthetic-password"
    assert connect_options["connect_timeout"] == verification_module.CONNECT_TIMEOUT_SECONDS
    for query, params in cursor.executed:
        assert query.lstrip().startswith("SELECT ") or query == "SHOW GRANTS"
        assert "INFORMATION_SCHEMA" in query or query.startswith("SELECT VERSION()") or query == "SHOW GRANTS"
        assert params == ("solog_import_stage",) or params == (
            "solog_import_stage",
            "%auto_increment%",
        ) or params is None


def test_privilege_verification_unavailable_blocks_schema_queries_and_closes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor(grants_error=pymysql.MySQLError("synthetic"))
    connection = FakeConnection(cursor)

    def connector(**kwargs: object) -> FakeConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        verification_module.pymysql,
        "connect",
        connector,
    )

    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "BLOCKED"
    assert result.privileges_status == "PRIVILEGES_UNVERIFIED"
    assert "SCHEMA_METADATA_COLLECTED" not in result.statuses
    assert len(cursor.executed) == 2
    assert connection.closed is True
    assert cursor.closed is True


def test_write_privileges_block_metadata_queries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor(
        grants=[
            "GRANT SELECT, INSERT ON `solog_import_stage`.* "
            "TO `importer_test`@`%`"
        ]
    )
    connection = FakeConnection(cursor)

    def connector(**kwargs: object) -> FakeConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        verification_module.pymysql,
        "connect",
        connector,
    )

    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "BLOCKED"
    assert result.privileges_status == "PRIVILEGES_VERIFIED"
    assert result.write_privileges_detected is True
    assert result.error_category == "WRITE_PRIVILEGES_DETECTED"
    assert len(cursor.executed) == 2


def test_global_read_grant_is_not_least_privilege_and_blocks_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor(
        grants=[
            "GRANT USAGE ON *.* TO `importer_test`@`%`",
            "GRANT SELECT ON `solog_import_stage`.* TO `importer_test`@`%`",
            "GRANT SELECT ON *.* TO `importer_test`@`%`",
        ]
    )
    connection = FakeConnection(cursor)

    def connector(**kwargs: object) -> FakeConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(verification_module.pymysql, "connect", connector)
    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "BLOCKED"
    assert result.privileges_status == "PRIVILEGES_VERIFIED"
    assert result.write_privileges_detected is False
    assert result.error_category == "NON_LEAST_PRIVILEGE_GRANTS"
    assert len(cursor.executed) == 2


def test_unrecognized_role_grant_is_unverified_and_blocks_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor(
        grants=[
            "GRANT `schema_reader` TO `importer_test`@`%`"
        ]
    )
    connection = FakeConnection(cursor)

    def connector(**kwargs: object) -> FakeConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        verification_module.pymysql,
        "connect",
        connector,
    )

    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "BLOCKED"
    assert result.privileges_status == "PRIVILEGES_UNVERIFIED"
    assert result.write_privileges_detected is False
    assert len(cursor.executed) == 2


def test_identity_mismatch_blocks_grants_and_schema_queries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = build_profile()
    cursor = FakeCursor(
        identity=(
            "10.11.6-MariaDB",
            "different_database",
            "target-server",
            3307,
            "importer_test@%",
            "importer_test@localhost",
        )
    )
    connection = FakeConnection(cursor)

    def connector(**kwargs: object) -> FakeConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        verification_module.pymysql,
        "connect",
        connector,
    )

    result = verification_module.TargetDatabaseVerificationService().verify(
        profile,
        "synthetic-password",
    )

    assert result.status == "IDENTITY_MISMATCH"
    assert result.identity is not None
    assert result.identity.database == "different_database"
    assert len(cursor.executed) == 1
    assert connection.closed is True


def test_alias_of_protected_reference_database_is_rejected_by_profile_model() -> None:
    with pytest.raises(ValueError, match="database referensi"):
        build_profile(
            host="localhost",
            port=3306,
            database="DB_SOLOG_OLI_INITIAL",
        )


def test_verification_endpoint_keeps_csrf_and_same_origin_protections(
    client: TestClient,
    target_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = selected_profile(target_data_dir)
    stub = StubVerificationService()
    monkeypatch.setattr(verification_router, "verification_service", stub)
    client.get("/target-databases/verify")
    token = verification_module.create_verification_form_token(profile)
    csrf_token = client.cookies.get("solog_csrf", "")
    form = {
        "password": "synthetic",
        "confirm_target": "yes",
        "verification_token": token,
        "csrf_token": csrf_token,
    }

    cross_origin = client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data=form,
        headers={"Origin": "https://attacker.example"},
    )
    missing_csrf = client.post(
        f"/target-databases/{profile.profile_id}/verify",
        data={**form, "csrf_token": ""},
        headers={"Origin": "http://localhost"},
    )

    assert cross_origin.status_code == 403
    assert missing_csrf.status_code == 403
    assert stub.calls == []


def test_verification_page_keeps_existing_security_headers(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    response = client.get("/target-databases/verify")

    assert response.status_code == 200
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"
