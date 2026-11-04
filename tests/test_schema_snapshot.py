import hashlib
import json
from pathlib import Path
from uuid import uuid4

import pymysql
import pytest

from app.models.target_database import TargetDatabaseProfile, TargetEnvironment
from app.services.schema_snapshot import (
    SchemaSnapshotStorage,
    SchemaSnapshotStorageError,
    TargetSchemaSnapshot,
    extract_view_dependencies,
)
from app.services.target_database_verification import (
    SchemaSnapshotCollectionError,
    TargetDatabaseVerificationService,
)


def build_target_profile() -> TargetDatabaseProfile:
    return TargetDatabaseProfile(
        profile_id=uuid4(),
        name="Synthetic local target",
        environment=TargetEnvironment.LOCAL,
        host="127.0.0.1",
        port=3306,
        database="solog_importer_1",
        username="devro",
    )


class SnapshotCursor:
    def __init__(
        self,
        *,
        hostname: str = "LAPTOP-H752SMP0",
        grants: list[str] | None = None,
        metadata_error: Exception | None = None,
        view_dependencies_error: Exception | None = None,
        unsafe_view_definition: str | None = None,
    ) -> None:
        self.identity = (
            "10.4.32-MariaDB",
            "solog_importer_1",
            hostname,
            3306,
            "devro@127.0.0.1",
            "devro@localhost",
        )
        self.grants = grants or [
            "GRANT USAGE ON *.* TO `devro`@`localhost`",
            "GRANT SELECT ON `solog_importer_1`.* TO `devro`@`localhost`",
            "GRANT SHOW VIEW ON `solog_importer_1`.* TO `devro`@`localhost`",
        ]
        self.metadata_error = metadata_error
        self.view_dependencies_error = view_dependencies_error
        self.unsafe_view_definition = unsafe_view_definition
        self.executed: list[tuple[str, tuple[object, ...] | None]] = []
        self.rows: list[tuple[object, ...]] = []
        self.closed = False

    def execute(
        self,
        query: str,
        params: tuple[object, ...] | None = None,
    ) -> None:
        self.executed.append((query, params))
        if query.startswith("SELECT VERSION()"):
            self.rows = [self.identity]
        elif query == "SHOW GRANTS":
            self.rows = [(grant,) for grant in self.grants]
        elif "INFORMATION_SCHEMA.COLUMNS" in query:
            self.rows = [
                (
                    "headers", "id", 1, "int", "int(11)", None, 10, 0,
                    "NO", None, "auto_increment", None, None, "", "BASE TABLE",
                ),
                (
                    "receipt_view", "label", 1, "varchar", "varchar(40)", 40,
                    None, None, "YES", None, "", "utf8mb4", "utf8mb4_general_ci",
                    "", "VIEW",
                ),
            ]
        elif "INFORMATION_SCHEMA.TABLES" in query:
            if self.metadata_error:
                raise self.metadata_error
            self.rows = [("headers", "InnoDB", "utf8mb4_general_ci", "", 42)]
        elif "REFERENCED_TABLE_NAME IS NOT NULL" in query:
            self.rows = [
                (
                    "headers", "warehouse_id", "warehouses", "id",
                    "fk_headers_warehouse", "RESTRICT", "CASCADE", 1,
                )
            ]
        elif "CONSTRAINT_NAME = 'PRIMARY'" in query:
            self.rows = [("headers", "PRIMARY", "id", 1)]
        elif "INFORMATION_SCHEMA.STATISTICS" in query:
            self.rows = [
                ("headers", "PRIMARY", 0, "BTREE", "id", 1, 1),
                ("headers", "uq_headers_number", 0, "BTREE", "number", 1, 1),
            ]
        elif "INFORMATION_SCHEMA.TABLE_CONSTRAINTS" in query:
            self.rows = [(1,)]
        elif "INFORMATION_SCHEMA.VIEWS" in query:
            self.rows = [
                (
                    "receipt_view",
                    "devro@localhost",
                    "DEFINER",
                    "NONE",
                    self.unsafe_view_definition
                    or "select `headers`.`id` AS `label` from `headers`",
                )
            ]
        elif "INFORMATION_SCHEMA.VIEW_TABLE_USAGE" in query:
            if self.view_dependencies_error:
                raise self.view_dependencies_error
            self.rows = [("receipt_view", "solog_importer_1", "headers")]
        elif query.startswith("SHOW CREATE VIEW"):
            self.rows = [
                (
                    "receipt_view",
                    "CREATE ALGORITHM=UNDEFINED DEFINER=`devro`@`localhost` "
                    "SQL SECURITY DEFINER VIEW `receipt_view` AS SELECT "
                    "`headers`.`id` AS `label` FROM `headers`",
                    "utf8mb4",
                    "utf8mb4_general_ci",
                )
            ]
        else:
            raise AssertionError(f"Unexpected query: {query}")

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return list(self.rows)

    def close(self) -> None:
        self.closed = True


class SnapshotConnection:
    def __init__(self, cursor: SnapshotCursor) -> None:
        self.snapshot_cursor = cursor
        self.closed = False

    def cursor(self) -> SnapshotCursor:
        return self.snapshot_cursor

    def close(self) -> None:
        self.closed = True


def collect_snapshot(
    monkeypatch: pytest.MonkeyPatch,
    cursor: SnapshotCursor,
    *,
    password: str = "",
) -> tuple[TargetSchemaSnapshot, SnapshotConnection, dict[str, object]]:
    profile = build_target_profile()
    connection = SnapshotConnection(cursor)
    options: dict[str, object] = {}

    def connector(**kwargs: object) -> SnapshotConnection:
        options.update(kwargs)
        return connection

    monkeypatch.setattr(
        "app.services.target_database_verification.pymysql.connect",
        connector,
    )
    snapshot = TargetDatabaseVerificationService().collect_schema_snapshot(
        profile,
        password,
        expected_hostname="LAPTOP-H752SMP0",
        expected_engine_version_prefix="10.4.32-MariaDB",
        expected_authenticated_user="devro@localhost",
        expected_effective_user="devro@127.0.0.1",
    )
    return snapshot, connection, options


def test_snapshot_collects_object_metadata_and_verifies_identity_and_grants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor()
    snapshot, connection, options = collect_snapshot(monkeypatch, cursor)

    assert snapshot.schema_version == 1
    assert snapshot.collection_status == "COMPLETE"
    assert snapshot.target.identity.database == "solog_importer_1"
    assert snapshot.target.identity.authenticated_user == "devro@localhost"
    assert snapshot.target.identity.effective_user == "devro@127.0.0.1"
    assert snapshot.target.verification.statuses == [
        "IDENTITY_VERIFIED",
        "PRIVILEGES_VERIFIED",
    ]
    assert snapshot.target.verification.allowed_privileges == ["SELECT", "SHOW VIEW"]
    assert snapshot.summary.base_tables == 1
    assert snapshot.summary.views == 1
    assert snapshot.summary.columns_total == 2
    assert snapshot.summary.primary_key_constraints == 1
    assert snapshot.summary.foreign_key_constraints == 1
    assert snapshot.summary.unique_indexes_excluding_primary == 1
    assert snapshot.summary.unique_constraints == 1
    assert snapshot.summary.auto_increment_tables == 1
    assert snapshot.columns[0].default_value is None
    assert snapshot.tables[0].auto_increment_value == 42
    assert snapshot.views[0].dependencies[0].table_name == "headers"
    assert options["password"] == ""
    assert connection.closed and cursor.closed
    assert all(
        query.startswith("SELECT VERSION()")
        or query == "SHOW GRANTS"
        or "INFORMATION_SCHEMA" in query
        for query, _ in cursor.executed
    )


def test_identity_mismatch_stops_before_grants_and_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor(hostname="different-server")
    connection = SnapshotConnection(cursor)

    def connector(**kwargs: object) -> SnapshotConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        "app.services.target_database_verification.pymysql.connect",
        connector,
    )

    with pytest.raises(SchemaSnapshotCollectionError) as error:
        TargetDatabaseVerificationService().collect_schema_snapshot(
            build_target_profile(),
            "",
            expected_hostname="LAPTOP-H752SMP0",
            expected_engine_version_prefix="10.4.32-MariaDB",
            expected_authenticated_user="devro@localhost",
            expected_effective_user="devro@127.0.0.1",
        )

    assert error.value.category == "IDENTITY_MISMATCH"
    assert [query for query, _ in cursor.executed] == [
        "SELECT VERSION(), DATABASE(), @@hostname, @@port, "
        "CURRENT_USER(), USER()"
    ]
    assert connection.closed and cursor.closed


def test_unapproved_privileges_stop_before_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor(
        grants=[
            "GRANT SELECT, INSERT ON `solog_importer_1`.* "
            "TO `devro`@`localhost`"
        ]
    )
    connection = SnapshotConnection(cursor)

    def connector(**kwargs: object) -> SnapshotConnection:
        _ = kwargs
        return connection

    monkeypatch.setattr(
        "app.services.target_database_verification.pymysql.connect",
        connector,
    )

    with pytest.raises(SchemaSnapshotCollectionError) as error:
        TargetDatabaseVerificationService().collect_schema_snapshot(
            build_target_profile(),
            "",
            expected_hostname="LAPTOP-H752SMP0",
            expected_engine_version_prefix="10.4.32-MariaDB",
            expected_authenticated_user="devro@localhost",
            expected_effective_user="devro@127.0.0.1",
        )

    assert error.value.category == "PRIVILEGES_BLOCKED"
    assert len(cursor.executed) == 2
    assert connection.closed and cursor.closed


def test_metadata_query_failure_is_recorded_as_gap_without_fabricated_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor(metadata_error=pymysql.MySQLError("synthetic"))
    snapshot, _, _ = collect_snapshot(monkeypatch, cursor)

    assert snapshot.collection_status == "PARTIAL"
    assert snapshot.summary.base_tables is None
    assert any(gap.component == "tables" for gap in snapshot.metadata_gaps)


def test_snapshot_derives_dependencies_from_view_definition_without_extra_metadata_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor()
    snapshot, _, _ = collect_snapshot(monkeypatch, cursor)

    assert snapshot.collection_status == "COMPLETE"
    assert [
        (dependency.schema_name, dependency.table_name)
        for dependency in snapshot.views[0].dependencies
    ] == [("solog_importer_1", "headers")]
    assert not any(
        "VIEW_TABLE_USAGE" in query
        for query, _ in cursor.executed
    )


def test_dependency_investigation_uses_show_create_after_missing_metadata_table(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor(
        view_dependencies_error=pymysql.err.ProgrammingError(
            1109,
            "Unknown table 'VIEW_TABLE_USAGE' in information_schema",
        )
    )
    connection = SnapshotConnection(cursor)
    options: dict[str, object] = {}

    def connector(**kwargs: object) -> SnapshotConnection:
        options.update(kwargs)
        return connection

    monkeypatch.setattr(
        "app.services.target_database_verification.pymysql.connect",
        connector,
    )
    result = TargetDatabaseVerificationService().investigate_view_dependencies(
        build_target_profile(),
        "",
        expected_hostname="LAPTOP-H752SMP0",
        expected_engine_version_prefix="10.4.32-MariaDB",
        expected_authenticated_user="devro@localhost",
        expected_effective_user="devro@127.0.0.1",
    )

    assert result.view_names == ["receipt_view"]
    assert result.view_table_usage_available is False
    assert result.view_table_usage_error_code == 1109
    assert result.show_create_definitions["receipt_view"].startswith(
        "CREATE ALGORITHM=UNDEFINED"
    )
    assert options["password"] == ""
    assert connection.closed and cursor.closed
    queries = [query for query, _ in cursor.executed]
    assert queries.index("SHOW GRANTS") < next(
        index for index, query in enumerate(queries)
        if "INFORMATION_SCHEMA.VIEWS" in query
    )
    assert any(query.startswith("SHOW CREATE VIEW") for query in queries)


def test_view_definition_dependency_extraction_ignores_literals_and_captures_nested_sources() -> None:
    dependencies = extract_view_dependencies(
        """
        SELECT 'FROM `not_a_table`' AS label
        FROM (((`target`.`headers` h
          JOIN `target`.`details` d ON d.header_id = h.id)
          LEFT JOIN (SELECT x.id FROM `target`.`extra` x) e ON e.id = h.id)
        """,
        "target",
    )

    assert {
        (dependency.schema_name, dependency.table_name)
        for dependency in dependencies
    } == {
        ("target", "headers"),
        ("target", "details"),
        ("target", "extra"),
    }


def test_view_definition_with_credential_pattern_is_omitted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = SnapshotCursor(
        unsafe_view_definition="select 'secret-value' AS label /* password='secret-value' */"
    )
    snapshot, _, _ = collect_snapshot(monkeypatch, cursor)

    assert snapshot.collection_status == "PARTIAL"
    assert snapshot.views[0].definition is None
    assert "secret-value" not in snapshot.model_dump_json()


def test_snapshot_is_validated_checksummed_and_not_overwritten(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    snapshot, _, _ = collect_snapshot(monkeypatch, SnapshotCursor())
    storage = SchemaSnapshotStorage(tmp_path / "data")
    path, digest = storage.save(snapshot, timestamp="20261104-120000")

    payload = path.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == digest
    assert path.with_suffix(".json.sha256").read_text(encoding="ascii") == (
        f"{digest}  {path.name}\n"
    )
    restored = TargetSchemaSnapshot.model_validate_json(payload)
    assert restored.summary.columns_total == 2
    assert "password" not in json.loads(payload).keys()
    with pytest.raises(SchemaSnapshotStorageError, match="sudah digunakan"):
        storage.save(snapshot, timestamp="20261104-120000")
