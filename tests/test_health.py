from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, base_url="http://localhost")


def test_health_endpoint_reports_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["application"] == "Solog OLI Migration Importer"


def test_dashboard_links_to_workbooks_without_import_action() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Solog OLI Migration Importer" in response.text
    assert 'hx-get="/health/status"' in response.text
    assert 'href="/workbooks"' in response.text
    assert "Belum ada laporan" in response.text
    assert ">Import<" not in response.text
    assert "hx-post" not in response.text
    assert "<form" not in response.text


def test_health_status_fragment_is_available_for_htmx() -> None:
    response = client.get("/health/status")

    assert response.status_code == 200
    assert 'id="app-status"' in response.text
    assert "Aplikasi aktif" in response.text
