import json
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.target_database_storage import TargetDatabaseStorage
import app.services.target_database_storage as target_storage_module


@pytest.fixture
def target_data_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    monkeypatch.setattr(target_storage_module, "DATA_DIR", data_dir)
    return data_dir


@pytest.fixture
def client() -> TestClient:
    return TestClient(app, base_url="http://localhost")


def valid_profile_data(**overrides: str) -> dict[str, str]:
    data = {
        "name": "Local staging target",
        "environment": "Staging",
        "host": "db-target.test",
        "port": "3307",
        "database": "solog_import_stage",
        "username": "importer_test",
        "password": "synthetic-secret-never-store",
    }
    data.update(overrides)
    return data


def post_form(
    client: TestClient,
    path: str,
    data: dict[str, str],
    *,
    origin: str = "http://localhost",
):
    client.get("/target-databases")
    return client.post(
        path,
        data={**data, "csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": origin},
        follow_redirects=False,
    )


def test_target_configuration_page_loads_without_reference_default(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    response = client.get("/target-databases")

    assert response.status_code == 200
    assert "Buat profil target" in response.text
    assert "Belum ada target yang dipilih" in response.text
    assert "TARGET terpilih" not in response.text
    assert TargetDatabaseStorage(target_data_dir).load().selected_profile_id is None


def test_valid_profile_is_created_without_selecting_it_or_persisting_password(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    response = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(name="<script>target</script>"),
    )

    storage = TargetDatabaseStorage(target_data_dir)
    configuration = storage.load()
    persisted = storage.configuration_path.read_text(encoding="utf-8")
    assert response.status_code == 303
    assert len(configuration.profiles) == 1
    assert configuration.profiles[0].purpose == "TARGET"
    assert configuration.selected_profile_id is None
    assert "synthetic-secret-never-store" not in persisted
    assert "synthetic-secret-never-store" not in response.text
    listing = client.get("/target-databases")
    assert "<script>target</script>" not in listing.text
    assert "&lt;script&gt;target&lt;/script&gt;" in listing.text


def test_unsupported_environment_and_unsafe_identity_fields_are_rejected(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    unsupported_environment = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(environment="Outside"),
    )
    unsafe_host = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(name="Safe host", host="db-target.test/path"),
    )
    unsafe_database = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(name="Safe database", database="bad/name"),
    )

    assert unsupported_environment.status_code == 422
    assert "Environment harus Local" in unsupported_environment.text
    assert unsafe_host.status_code == 422
    assert "Konfigurasi profil tidak valid" in unsafe_host.text
    assert unsafe_database.status_code == 422
    assert "Konfigurasi profil tidak valid" in unsafe_database.text
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("name", "Nama profil wajib diisi"),
        ("environment", "Environment harus Local"),
        ("host", "Host wajib diisi"),
        ("database", "Nama database wajib diisi"),
        ("username", "Username wajib diisi"),
    ],
)
def test_missing_required_fields_are_rejected(
    client: TestClient,
    target_data_dir: Path,
    field: str,
    message: str,
) -> None:
    response = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(**{field: ""}),
    )

    assert response.status_code == 422
    assert message in response.text
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


@pytest.mark.parametrize("port", ["0", "-1", "65536", "3306.5", "abc", ""])
def test_invalid_ports_are_rejected(
    client: TestClient,
    target_data_dir: Path,
    port: str,
) -> None:
    response = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(port=port),
    )

    assert response.status_code == 422
    assert "Port harus berupa bilangan bulat" in response.text
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


def test_duplicate_profile_name_is_rejected_case_insensitively(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    first = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(),
    )
    second = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(name="LOCAL STAGING TARGET"),
    )

    assert first.status_code == 303
    assert second.status_code == 409
    assert "Nama profil target sudah digunakan" in second.text
    assert len(TargetDatabaseStorage(target_data_dir).load().profiles) == 1


def test_list_and_detail_never_expose_password(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    post_form(client, "/target-databases/create", valid_profile_data())
    profile = TargetDatabaseStorage(target_data_dir).load().profiles[0]

    listing = client.get("/target-databases")
    detail = client.get(f"/target-databases/{profile.profile_id}")

    assert listing.status_code == 200
    assert detail.status_code == 200
    assert "synthetic-secret-never-store" not in listing.text
    assert "synthetic-secret-never-store" not in detail.text
    assert "Password (opsional; tidak disimpan)" in listing.text
    assert "Password baru (opsional; tidak disimpan)" in detail.text


@pytest.mark.parametrize(
    ("host", "database"),
    [
        ("LAPTOP-H752SMP0", "db_solog_oli_initial"),
        ("127.0.0.1", "db_solog_oli_initial"),
        ("localhost", "db_solog_oli_initial"),
        ("laptop-h752smp0.", "DB_SOLOG_OLI_INITIAL"),
    ],
)
def test_reference_database_identity_is_rejected(
    client: TestClient,
    target_data_dir: Path,
    host: str,
    database: str,
) -> None:
    response = post_form(
        client,
        "/target-databases/create",
        valid_profile_data(host=host, port="3306", database=database),
    )

    assert response.status_code == 422
    assert "database referensi tidak dapat digunakan sebagai TARGET" in response.text
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


def test_profile_can_be_selected_and_is_shown_as_explicit_target(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    post_form(client, "/target-databases/create", valid_profile_data())
    profile = TargetDatabaseStorage(target_data_dir).load().profiles[0]
    selection = post_form(
        client,
        f"/target-databases/{profile.profile_id}/select",
        {},
    )
    page = client.get("/target-databases")

    assert selection.status_code == 303
    assert TargetDatabaseStorage(target_data_dir).load().selected_profile_id == profile.profile_id
    assert "TARGET TERPILIH" in page.text
    assert "db-target.test:3307/solog_import_stage" in page.text
    assert "Purpose:" in page.text


def test_edit_action_is_available_for_selected_and_unselected_profiles(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    post_form(client, "/target-databases/create", valid_profile_data())
    first_profile = TargetDatabaseStorage(target_data_dir).load().profiles[0]
    post_form(
        client,
        "/target-databases/create",
        valid_profile_data(name="Second target", host="second-db-target.test"),
    )
    second_profile = next(
        profile
        for profile in TargetDatabaseStorage(target_data_dir).load().profiles
        if profile.profile_id != first_profile.profile_id
    )
    post_form(
        client,
        f"/target-databases/{first_profile.profile_id}/select",
        {},
    )

    listing = client.get("/target-databases")
    first_detail = client.get(f"/target-databases/{first_profile.profile_id}")
    second_detail = client.get(f"/target-databases/{second_profile.profile_id}")

    assert listing.status_code == 200
    assert listing.text.count(">Edit</a>") == 2
    assert f'href="/target-databases/{first_profile.profile_id}">Edit</a>' in listing.text
    assert f'href="/target-databases/{second_profile.profile_id}">Edit</a>' in listing.text
    assert first_detail.status_code == 200
    assert second_detail.status_code == 200
    update = post_form(
        client,
        f"/target-databases/{second_profile.profile_id}/update",
        valid_profile_data(name="Updated unselected", host="updated-target.test"),
    )
    configuration = TargetDatabaseStorage(target_data_dir).load()

    assert update.status_code == 303
    assert configuration.selected_profile_id == first_profile.profile_id
    assert next(
        profile
        for profile in configuration.profiles
        if profile.profile_id == second_profile.profile_id
    ).name == "Updated unselected"


def test_nonexistent_profile_cannot_be_selected(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    response = post_form(
        client,
        f"/target-databases/{uuid4()}/select",
        {},
    )

    assert response.status_code == 404
    assert TargetDatabaseStorage(target_data_dir).load().selected_profile_id is None


def test_invalid_persisted_profile_cannot_be_selected(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    target_data_dir.mkdir()
    profile_id = uuid4()
    (target_data_dir / "target-databases.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "profiles": [
                    {
                        "profile_id": str(profile_id),
                        "name": "Incomplete profile",
                        "environment": "Staging",
                        "host": "db-target.test",
                        "port": 70000,
                        "database": "stage",
                        "username": "user",
                        "purpose": "TARGET",
                    }
                ],
                "selected_profile_id": None,
            }
        ),
        encoding="utf-8",
    )

    response = post_form(
        client,
        f"/target-databases/{profile_id}/select",
        {},
    )

    assert response.status_code == 500
    assert TargetDatabaseStorage(target_data_dir).configuration_path.read_text(
        encoding="utf-8"
    ).find('"selected_profile_id": null') >= 0


def test_profile_settings_can_be_edited_without_retaining_password(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    post_form(client, "/target-databases/create", valid_profile_data())
    profile = TargetDatabaseStorage(target_data_dir).load().profiles[0]
    post_form(client, f"/target-databases/{profile.profile_id}/select", {})
    response = post_form(
        client,
        f"/target-databases/{profile.profile_id}/update",
        valid_profile_data(
            name="Renamed target",
            host="edited-db-target.test",
            password="another-synthetic-secret",
        ),
    )

    configuration = TargetDatabaseStorage(target_data_dir).load()
    updated = configuration.profiles[0]
    persisted = TargetDatabaseStorage(target_data_dir).configuration_path.read_text(encoding="utf-8")
    assert response.status_code == 303
    assert updated.profile_id == profile.profile_id
    assert updated.name == "Renamed target"
    assert updated.host == "edited-db-target.test"
    assert updated.revision == profile.revision + 1
    assert configuration.selected_profile_id == profile.profile_id
    assert "another-synthetic-secret" not in persisted


def test_profile_delete_requires_confirmation_and_clears_selection(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    post_form(client, "/target-databases/create", valid_profile_data())
    profile = TargetDatabaseStorage(target_data_dir).load().profiles[0]
    post_form(client, f"/target-databases/{profile.profile_id}/select", {})

    unconfirmed = post_form(
        client,
        f"/target-databases/{profile.profile_id}/delete",
        {},
    )
    confirmed = post_form(
        client,
        f"/target-databases/{profile.profile_id}/delete",
        {"confirm_delete": "yes"},
    )
    configuration = TargetDatabaseStorage(target_data_dir).load()

    assert unconfirmed.status_code == 422
    assert confirmed.status_code == 303
    assert configuration.profiles == []
    assert configuration.selected_profile_id is None


def test_target_profile_posts_keep_same_origin_and_csrf_protections(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    csrf_token = client.get("/target-databases").cookies.get("solog_csrf", "")
    response = client.post(
        "/target-databases/create",
        data={**valid_profile_data(), "csrf_token": csrf_token},
        headers={"Origin": "https://attacker.example"},
    )

    assert response.status_code == 403
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []


def test_target_profile_post_requires_csrf_token(
    client: TestClient,
    target_data_dir: Path,
) -> None:
    client.get("/target-databases")
    response = client.post(
        "/target-databases/create",
        data=valid_profile_data(),
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 403
    assert "Token CSRF" in response.text
    assert TargetDatabaseStorage(target_data_dir).load().profiles == []
