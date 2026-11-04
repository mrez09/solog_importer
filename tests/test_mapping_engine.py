from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app
from app.models.mapping import (
    MappingDefinition,
    MappingOverride,
    MappingStatus,
    TargetDataType,
    ValidationSeverity,
)
from app.models.workbook import SourceLocator
from app.services.mapping_engine import (
    build_mapping_definitions,
    build_mapping_preview,
    validate_mapping,
    validate_mapping_candidates,
)
from app.services.mapping_storage import MappingStorage
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app, base_url="http://localhost")
MAPPING_STATUSES = {
    "DRAFT",
    "REVIEW_REQUIRED",
    "APPROVED",
    "REJECTED",
    "HOLD",
}


def build_mapping_workbook(detail_count: int = 1) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rincian Penerimaan Barang"
    sheet["C5"] = "Nomor #"
    sheet["E5"] = "RI.TEST.0001"
    sheet["J5"] = "Pemasok"
    sheet["N5"] = "Supplier Test"
    sheet["C6"] = "Tanggal"
    sheet["E6"] = datetime(2026, 1, 8)
    sheet["F7"] = "Kode #"
    sheet["H7"] = "Nama Barang"
    sheet["L7"] = "Kuantitas"
    sheet["P7"] = "Satuan"
    for row_number in range(8, 8 + detail_count):
        sheet.cell(row_number, 6, "ITEM-01")
        sheet.cell(row_number, 8, "Barang Test")
        sheet.cell(row_number, 12, 2)
    sheet.cell(8 + detail_count, 2, "Halaman 1")
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def upload_mapping_workbook(
    monkeypatch, tmp_path: Path, detail_count: int = 1
):
    import app.services.mapping_storage as mapping_storage_module
    import app.services.workbook_storage as workbook_storage_module

    data_dir = tmp_path / "isolated"
    monkeypatch.setattr(mapping_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "PROJECT_ROOT", tmp_path)
    content = build_mapping_workbook(detail_count)
    client.get("/workbooks")
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "OLI_GRN_mapping_fixture.xlsx",
                    content,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": "http://localhost"},
    )
    assert response.status_code == 201, response.text
    record = WorkbookStorage().list_workbooks()[0]
    return record, data_dir, content


def make_mapping(**overrides) -> MappingDefinition:
    values = {
        "mapping_id": "test-field-1",
        "candidate_kind": "detail",
        "source_field": "ri.detail.item_code",
        "source_value": "ITEM-01",
        "source_data_type": "s",
        "source_status": "PRESENT",
        "source_locator": SourceLocator(
            source_file_id="a" * 32,
            source_filename="source.xlsx",
            source_sha256="b" * 64,
            sheet_name="Rincian Penerimaan Barang",
            sheet_index=1,
            row_number=8,
            cell_coordinate="F8",
        ),
    }
    values.update(overrides)
    return MappingDefinition(**values)


def test_mapping_status_values_and_initial_status_are_review_required() -> None:
    assert MAPPING_STATUSES == {status.value for status in MappingStatus}
    assert make_mapping().status == MappingStatus.REVIEW_REQUIRED


def test_required_and_type_validation_produce_hold_without_changing_mapping_status() -> None:
    mapping = make_mapping(
        target_entity="item",
        target_field="code",
        target_required=True,
        target_data_type=TargetDataType.INTEGER,
    )

    validation = validate_mapping(mapping)

    codes = {issue.code for issue in validation.issues}
    assert {"data_type_mismatch"} <= codes
    assert validation.evaluation_status == "HOLD"
    assert mapping.status == MappingStatus.REVIEW_REQUIRED


def test_empty_required_value_is_error_and_optional_empty_value_is_warning() -> None:
    required = make_mapping(
        source_value=None,
        source_status="UNRESOLVED",
        target_entity="receipt",
        target_field="unit",
        target_required=True,
    )
    optional = make_mapping(
        mapping_id="optional-empty",
        source_value="",
        target_entity="receipt",
        target_field="unit_note",
        target_required=False,
    )

    required_result = validate_mapping(required)
    optional_result = validate_mapping(optional)

    assert any(issue.code == "required_field_empty" for issue in required_result.issues)
    assert required_result.evaluation_status == "HOLD"
    assert any(
        issue.code == "empty_source_value"
        and issue.severity == ValidationSeverity.WARNING
        for issue in optional_result.issues
    )


def test_unresolved_mapping_and_invalid_reference_are_held() -> None:
    mapping = make_mapping(
        allowed_references=["ITEM-02", "ITEM-03"],
        target_entity="items",
        target_field="code",
    )

    validation = validate_mapping(mapping)

    codes = {issue.code for issue in validation.issues}
    assert {"invalid_reference"} <= codes
    assert validation.evaluation_status == "HOLD"
    unresolved = validate_mapping(make_mapping())
    assert any(issue.code == "mapping_unresolved" for issue in unresolved.issues)
    assert unresolved.evaluation_status == "HOLD"


def test_duplicate_candidate_detection_does_not_remove_or_merge_source_rows() -> None:
    mapping = make_mapping()
    duplicate = mapping.model_copy(update={"mapping_id": "test-field-2"})
    validations = validate_mapping_candidates([mapping, duplicate])

    assert len(validations) == 2
    assert all(
        any(issue.code == "duplicate_mapping_candidate" for issue in result.issues)
        for result in validations
    )
    assert mapping.source_locator.cell_coordinate == "F8"
    assert duplicate.source_locator == mapping.source_locator


def test_explicit_hold_status_remains_on_hold() -> None:
    mapping = make_mapping(
        target_entity="item",
        target_field="code",
        status=MappingStatus.HOLD,
    )

    assert validate_mapping(mapping).evaluation_status == "HOLD"


def test_preview_preserves_source_locator_value_and_never_approves_automatically(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_mapping_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)

    definitions = build_mapping_definitions(analysis)
    preview = build_mapping_preview(analysis, {}, page=1)
    number_mapping = next(
        item for item in definitions if item.source_field == "ri.header.document_number"
    )
    number_row = next(
        row
        for row in preview.rows
        if row.mapping.source_field == "ri.header.document_number"
    )

    assert all(item.status == MappingStatus.REVIEW_REQUIRED for item in definitions)
    assert number_mapping.source_value == "RI.TEST.0001"
    assert number_mapping.source_locator is not None
    assert number_mapping.source_locator.cell_coordinate == "E5"
    assert number_mapping.source_locator.source_file_id == record.source_file_id
    assert number_row.mapping.source_value == "RI.TEST.0001"
    assert number_row.target_candidate is None
    assert number_row.validation.evaluation_status == "HOLD"
    assert preview.report.approved_mappings == 0
    assert preview.report.validation_hold_candidates > 0


def test_mapping_preview_paginates_candidates(monkeypatch, tmp_path: Path) -> None:
    record, _, _ = upload_mapping_workbook(monkeypatch, tmp_path, detail_count=7)
    analysis = WorkbookStorage().analyze_ri_layout(record)

    preview = build_mapping_preview(analysis, {}, page=2)

    assert preview.report.total_mapped_candidates == 31
    assert preview.page == 2
    assert preview.total_pages == 2
    assert len(preview.rows) == 6


def test_transformation_is_preview_only_and_original_value_is_retained(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_mapping_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    definition = next(
        item
        for item in build_mapping_definitions(analysis)
        if item.source_field == "ri.header.document_number"
    ).model_copy(update={"transformation_rule": "trim"})
    preview = build_mapping_preview(
        analysis,
        {
            definition.mapping_id: MappingOverride(
                mapping_id=definition.mapping_id,
                transformation_rule="trim",
            )
        },
    )

    row = next(
        row for row in preview.rows if row.mapping.mapping_id == definition.mapping_id
    )
    assert row.mapping.source_value == "RI.TEST.0001"
    assert row.transformation_preview == "trim (belum dijalankan)"
    assert any(issue.code == "transformation_not_executed" for issue in row.validation.issues)


def test_mapping_preview_endpoint_updates_local_profile_only_and_keeps_source_unchanged(
    monkeypatch, tmp_path: Path
) -> None:
    record, data_dir, original_content = upload_mapping_workbook(monkeypatch, tmp_path)
    source_path = data_dir / "uploads" / record.storage_filename
    source_hash = sha256(source_path.read_bytes()).hexdigest()

    response = client.get(f"/mappings/{record.source_file_id}")

    assert response.status_code == 200
    assert "Mapping &amp; validation" in response.text
    assert "RI.TEST.0001" in response.text
    assert "E5" in response.text
    assert "REVIEW_REQUIRED" in response.text
    assert "Validation report" in response.text

    update = client.post(
        f"/mappings/{record.source_file_id}/header-1-document_number",
        data={
            "target_entity": "receipt_placeholder",
            "target_field": "code_placeholder",
            "target_data_type": "string",
            "target_required": "yes",
            "allowed_references": "",
            "transformation_rule": "",
            "status": "DRAFT",
            "review_notes": "Target tetap placeholder untuk review.",
            "page": "1",
            "csrf_token": client.cookies.get("solog_csrf", ""),
        },
        headers={"Origin": "http://localhost"},
        follow_redirects=False,
    )

    assert update.status_code == 303
    profile = MappingStorage(data_dir).load_profile(
        record.source_file_id, record.source_sha256
    )
    override = profile.overrides["header-1-document_number"]
    assert override.status == MappingStatus.DRAFT
    assert override.target_entity == "receipt_placeholder"
    assert source_path.read_bytes() == original_content
    assert sha256(source_path.read_bytes()).hexdigest() == source_hash


def test_approved_status_requires_explicit_review_note(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_mapping_workbook(monkeypatch, tmp_path)
    client.get(f"/mappings/{record.source_file_id}")

    response = client.post(
        f"/mappings/{record.source_file_id}/header-1-document_number",
        data={
            "status": "APPROVED",
            "review_notes": "",
            "csrf_token": client.cookies.get("solog_csrf", ""),
        },
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 422
    assert "Catatan review wajib diisi" in response.text


def test_mapping_update_requires_csrf_token(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_mapping_workbook(monkeypatch, tmp_path)
    client.get(f"/mappings/{record.source_file_id}")

    response = client.post(
        f"/mappings/{record.source_file_id}/header-1-document_number",
        data={"status": "DRAFT", "review_notes": "Uji CSRF."},
        headers={"Origin": "http://localhost"},
    )

    assert response.status_code == 403
    assert "Token CSRF" in response.text
