from io import BytesIO

from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app, base_url="http://localhost")


def build_workbook() -> bytes:
    workbook = Workbook()
    workbook.active["A1"] = "Fixture"
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def test_security_headers_and_host_only_csrf_cookie_are_set() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["permissions-policy"] == "camera=(), microphone=(), geolocation=()"
    assert response.headers["cross-origin-resource-policy"] == "same-origin"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    cookie = response.headers["set-cookie"]
    assert "solog_csrf=" in cookie
    assert "httponly" in cookie.casefold()
    assert "samesite=strict" in cookie.casefold()
    assert "domain=" not in cookie.casefold()


def test_untrusted_host_is_rejected() -> None:
    response = client.get("/", headers={"Host": "attacker.example"})

    assert response.status_code == 400


def test_upload_requires_csrf_token_even_for_same_origin() -> None:
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "fixture.xlsx",
                    build_workbook(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 403
    assert "Token CSRF" in response.text


def test_upload_requires_origin_or_referer_when_csrf_token_is_present() -> None:
    client.get("/workbooks")
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "fixture.xlsx",
                    build_workbook(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
    )

    assert response.status_code == 403
    assert "lintas-origin" in response.text


def test_workbook_filename_is_escaped_in_html(monkeypatch, tmp_path) -> None:
    import app.services.workbook_storage as workbook_storage_module

    monkeypatch.setattr(workbook_storage_module, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(workbook_storage_module, "PROJECT_ROOT", tmp_path)
    client.get("/workbooks")
    upload = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    '<script>alert("x")</script>.xlsx',
                    build_workbook(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": "http://localhost"},
    )
    listing = client.get("/workbooks")

    assert upload.status_code == 201, upload.text
    assert listing.status_code == 200
    assert '<script>alert("x")</script>' not in listing.text
    assert "&lt;script&gt;" in listing.text


def test_report_endpoint_returns_json_attachment_with_security_headers(
    monkeypatch, tmp_path
) -> None:
    import app.services.mapping_storage as mapping_storage_module
    import app.services.workbook_storage as workbook_storage_module

    data_dir = tmp_path / "data"
    monkeypatch.setattr(mapping_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "PROJECT_ROOT", tmp_path)
    client.get("/workbooks")
    upload = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "OLI_GRN_report.xlsx",
                    build_workbook(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": "http://localhost"},
    )
    assert upload.status_code == 201
    workbook_id = WorkbookStorage().list_workbooks()[0].source_file_id

    response = client.get(f"/dry-run/{workbook_id}/report")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.headers["content-disposition"].endswith(".json\"")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.json()["source_file_id"] == workbook_id
