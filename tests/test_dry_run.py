import sqlite3
import socket
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app
from app.models.mapping import MappingOverride, MappingStatus, TargetDataType
from app.models.ri_candidate import RIAnalysisResult
from app.models.workbook import WorkbookRecord
from app.services.dry_run import build_dry_run, build_dry_run_report
from app.services.mapping_engine import build_mapping_definitions
from app.services.mapping_storage import MappingStorage
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app, base_url="http://localhost")


def build_preview_workbook(
    document_count: int = 1,
    *,
    include_unresolved_row: bool = False,
) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rincian Penerimaan Barang"
    for index in range(document_count):
        header_row = 5 + index * 7
        sheet.cell(header_row, 3, "Nomor #")
        sheet.cell(header_row, 5, f"RI.TEST.{index + 1:04d}")
        sheet.cell(header_row, 10, "Pemasok")
        sheet.cell(header_row, 14, "Supplier Test")
        sheet.cell(header_row + 1, 3, "Tanggal")
        sheet.cell(header_row + 1, 5, datetime(2026, 1, 8))
        sheet.cell(header_row + 2, 6, "Kode #")
        sheet.cell(header_row + 2, 8, "Nama Barang")
        sheet.cell(header_row + 2, 12, "Kuantitas")
        sheet.cell(header_row + 2, 16, "Satuan")
        sheet.cell(header_row + 3, 6, f"ITEM-{index + 1:02d}")
        sheet.cell(header_row + 3, 8, "Barang Test")
        sheet.cell(header_row + 3, 12, 2)
        sheet.cell(header_row + 3, 16, "pcs")
        sheet.cell(header_row + 4, 2, f"Halaman {index + 1}")
    if include_unresolved_row:
        unresolved_row = 5 + document_count * 7
        sheet.cell(unresolved_row, 6, "ITEM-UNRESOLVED")
        sheet.cell(unresolved_row, 8, "Detail tanpa header")
        sheet.cell(unresolved_row, 12, 3)
        sheet.cell(unresolved_row, 16, "pcs")
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def upload_preview_workbook(
    monkeypatch,
    tmp_path: Path,
    *,
    document_count: int = 1,
    include_unresolved_row: bool = False,
) -> tuple[WorkbookRecord, Path, bytes]:
    import app.services.mapping_storage as mapping_storage_module
    import app.services.workbook_storage as workbook_storage_module

    data_dir = tmp_path / "isolated"
    monkeypatch.setattr(mapping_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "PROJECT_ROOT", tmp_path)
    content = build_preview_workbook(
        document_count,
        include_unresolved_row=include_unresolved_row,
    )
    client.get("/workbooks")
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "OLI_GRN_dry_run_fixture.xlsx",
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


def make_approved_overrides(
    analysis: RIAnalysisResult,
    *,
    transform_mapping_id: str | None = None,
    invalid_type_mapping_id: str | None = None,
    hold_mapping_id: str | None = None,
) -> dict[str, MappingOverride]:
    overrides: dict[str, MappingOverride] = {}
    for mapping in build_mapping_definitions(analysis):
        overrides[mapping.mapping_id] = MappingOverride(
            mapping_id=mapping.mapping_id,
            target_entity="receipt_header" if mapping.candidate_kind == "header" else "receipt_detail",
            target_field=mapping.source_field.rsplit(".", 1)[-1],
            target_data_type=(
                TargetDataType.INTEGER
                if mapping.mapping_id == invalid_type_mapping_id
                else None
            ),
            transformation_rule=(
                "normalisasi deskriptif"
                if mapping.mapping_id == transform_mapping_id
                else None
            ),
            status=(
                MappingStatus.HOLD
                if mapping.mapping_id == hold_mapping_id
                else MappingStatus.APPROVED
            ),
            review_notes="Persetujuan eksplisit fixture test.",
        )
    return overrides


def test_synthetic_preview_preserves_raw_value_locator_and_source_fingerprint(
    monkeypatch, tmp_path: Path
) -> None:
    record, data_dir, original = upload_preview_workbook(monkeypatch, tmp_path)
    source_path = data_dir / "uploads" / record.storage_filename
    original_digest = sha256(original).hexdigest()
    analysis = WorkbookStorage().analyze_ri_layout(record)
    mapping = next(
        item
        for item in build_mapping_definitions(analysis)
        if item.source_field == "ri.header.document_number"
    )
    overrides = make_approved_overrides(
        analysis,
        transform_mapping_id=mapping.mapping_id,
    )

    preview = build_dry_run(analysis, overrides)
    report = build_dry_run_report(analysis, overrides)
    document = preview.candidates[0]
    row = next(item for item in document.mappings if item.mapping.mapping_id == mapping.mapping_id)
    payload = next(
        group
        for group in preview.entity_groups
        if group.target_entity_placeholder == "receipt_header"
    ).records[0]
    payload_field = next(item for item in payload.fields if item.mapping_id == mapping.mapping_id)

    assert preview.source_filename == record.source_filename
    assert preview.source_sha256 == record.source_sha256
    assert row.mapping.source_value == "RI.TEST.0001"
    assert row.mapping.source_locator is not None
    assert row.mapping.source_locator.cell_coordinate == "E5"
    assert row.transformation_planned == "normalisasi deskriptif"
    assert row.transformation_executed is False
    assert payload_field.raw_source_value == "RI.TEST.0001"
    assert payload_field.transformation_executed is False
    assert report.source_sha256 == record.source_sha256
    assert source_path.read_bytes() == original
    assert sha256(source_path.read_bytes()).hexdigest() == original_digest


def test_incomplete_mapping_is_held_and_audited_with_source_locator(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)

    preview = build_dry_run(analysis)
    report = build_dry_run_report(analysis)
    mapping_finding = next(
        finding for finding in report.findings if finding.code == "mapping_unresolved"
    )

    assert preview.summary.total_source_candidates == 1
    assert preview.summary.total_mappings == 7
    assert preview.summary.hold_candidates == 1
    assert preview.summary.candidates_without_target_mapping == 1
    assert preview.summary.candidates_without_approval == 1
    assert preview.candidates[0].status == "HOLD"
    assert mapping_finding.source_locator is not None
    assert mapping_finding.source_locator.cell_coordinate == "E5"


def test_unresolved_stage_423_row_remains_a_separate_held_candidate(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(
        monkeypatch,
        tmp_path,
        include_unresolved_row=True,
    )
    analysis = WorkbookStorage().analyze_ri_layout(record)

    result = build_dry_run(analysis)
    unresolved = next(
        candidate
        for candidate in result.candidates
        if candidate.candidate_kind == "unresolved_row"
    )

    assert result.summary.total_source_candidates == 2
    assert unresolved.status == "HOLD"
    assert unresolved.source_row == 12
    assert all(
        mapping.mapping.source_candidate_id == unresolved.candidate_id
        for mapping in unresolved.mappings
    )
    assert unresolved.mappings[0].mapping.source_locator is not None
    assert unresolved.mappings[0].mapping.source_locator.row_number == 12


def test_review_required_mapping_is_never_counted_as_approved(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    definitions = build_mapping_definitions(analysis)
    overrides = {
        mapping.mapping_id: MappingOverride(
            mapping_id=mapping.mapping_id,
            target_entity="receipt",
            target_field="placeholder",
            status=MappingStatus.REVIEW_REQUIRED,
        )
        for mapping in definitions
    }

    result = build_dry_run(analysis, overrides)

    assert result.summary.hold_candidates == 1
    assert result.summary.candidates_without_approval == 1
    assert result.summary.mappings_without_approval == len(definitions)
    assert all(
        mapping.mapping.status == MappingStatus.REVIEW_REQUIRED
        for mapping in result.candidates[0].mappings
    )


def test_explicitly_approved_complete_mappings_can_validate_but_not_approve_import(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    result = build_dry_run(analysis, make_approved_overrides(analysis))

    assert result.candidates[0].status == "VALID"
    assert result.summary.valid_candidates == 1
    assert result.summary.candidates_without_approval == 0
    assert result.relationships[0].status == "UNKNOWN"
    assert result.relationships[0].disposition == "HOLD"
    assert "bukan" not in result.relationships[0].reason.casefold()
    assert "REL-01" in result.relationships[0].reason


def test_explicit_mapping_hold_remains_hold(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    mapping_id = build_mapping_definitions(analysis)[0].mapping_id
    result = build_dry_run(
        analysis,
        make_approved_overrides(analysis, hold_mapping_id=mapping_id),
    )

    assert result.candidates[0].status == "HOLD"
    assert result.summary.hold_candidates == 1


def test_validation_error_and_warning_are_reported_without_transforming_values(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    definitions = build_mapping_definitions(analysis)
    number_mapping = next(
        item for item in definitions if item.source_field == "ri.header.document_number"
    )
    quantity_mapping = next(
        item for item in definitions if item.source_field == "ri.detail.quantity"
    )
    overrides = make_approved_overrides(
        analysis,
        transform_mapping_id=quantity_mapping.mapping_id,
        invalid_type_mapping_id=number_mapping.mapping_id,
    )

    result = build_dry_run(analysis, overrides)
    report = build_dry_run_report(analysis, overrides)
    issue_codes = {finding.code for finding in report.findings}

    assert result.candidates[0].status == "ERROR"
    assert result.summary.error_candidates == 1
    assert result.summary.validation_error_count > 0
    assert result.summary.validation_warning_count > 0
    assert "data_type_mismatch" in issue_codes
    assert "transformation_not_executed" in issue_codes
    quantity_preview = next(
        mapping
        for mapping in result.candidates[0].mappings
        if mapping.mapping.mapping_id == quantity_mapping.mapping_id
    )
    assert quantity_preview.mapping.source_value == 2
    assert quantity_preview.transformation_executed is False


def test_transformation_warning_is_a_warning_candidate(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)
    analysis = WorkbookStorage().analyze_ri_layout(record)
    transform_id = next(
        item.mapping_id
        for item in build_mapping_definitions(analysis)
        if item.source_field == "ri.header.document_number"
    )

    result = build_dry_run(
        analysis,
        make_approved_overrides(
            analysis,
            transform_mapping_id=transform_id,
        ),
    )

    assert result.candidates[0].status == "WARNING"
    assert result.summary.warning_candidates == 1


def test_source_locator_and_unknown_relationship_are_in_html_preview(
    monkeypatch, tmp_path: Path
) -> None:
    record, _, _ = upload_preview_workbook(monkeypatch, tmp_path)

    response = client.get(f"/dry-run/{record.source_file_id}")

    assert response.status_code == 200
    assert "RI.TEST.0001" in response.text
    assert "Rincian Penerimaan Barang!E5" in response.text
    assert "PO–RI" in response.text
    assert "UNKNOWN" in response.text
    assert "/sheets/1/preview?start_row=5" in response.text


def test_preview_does_not_connect_to_database_or_change_mapping_profile(
    monkeypatch, tmp_path: Path
) -> None:
    record, data_dir, original = upload_preview_workbook(monkeypatch, tmp_path)
    storage = MappingStorage(data_dir)
    profile = storage.load_profile(record.source_file_id, record.source_sha256)
    definition = build_mapping_definitions(
        WorkbookStorage().analyze_ri_layout(record)
    )[0]
    profile.overrides[definition.mapping_id] = MappingOverride(
        mapping_id=definition.mapping_id,
        status=MappingStatus.REVIEW_REQUIRED,
        review_notes="Tetap perlu review.",
    )
    storage.save_profile(profile)
    before_profile = storage.load_profile(record.source_file_id, record.source_sha256)
    source_path = data_dir / "uploads" / record.storage_filename

    def forbidden(*_args, **_kwargs):
        _ = _args, _kwargs
        raise AssertionError("Dry-run tidak boleh membuka koneksi database/jaringan.")

    monkeypatch.setattr(sqlite3, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)

    response = client.get(f"/dry-run/{record.source_file_id}")
    report_response = client.get(f"/dry-run/{record.source_file_id}/report")

    after_profile = storage.load_profile(record.source_file_id, record.source_sha256)
    assert response.status_code == 200
    assert report_response.status_code == 200
    assert report_response.json()["source_sha256"] == record.source_sha256
    assert report_response.headers["content-disposition"].endswith(".json\"")
    assert before_profile.model_dump(mode="json") == after_profile.model_dump(mode="json")
    assert source_path.read_bytes() == original


def test_candidate_pagination_and_status_filter_are_available_in_ui(
    monkeypatch, tmp_path: Path
) -> None:
    record, data_dir, _ = upload_preview_workbook(
        monkeypatch,
        tmp_path,
        document_count=26,
    )
    analysis = WorkbookStorage().analyze_ri_layout(record)
    overrides = make_approved_overrides(analysis)
    first_mapping = build_mapping_definitions(analysis)[0]
    overrides[first_mapping.mapping_id].status = MappingStatus.REVIEW_REQUIRED
    profile = MappingStorage(data_dir).load_profile(
        record.source_file_id,
        record.source_sha256,
    )
    profile.overrides = overrides
    MappingStorage(data_dir).save_profile(profile)

    paginated = client.get(f"/dry-run/{record.source_file_id}?page=2&status=ALL")
    filtered = client.get(f"/dry-run/{record.source_file_id}?status=HOLD")

    assert paginated.status_code == 200
    assert "Halaman 2 / 2" in paginated.text
    assert "Filter status" in paginated.text
    assert filtered.status_code == 200
    assert "filter HOLD" in filtered.text
    assert "Kandidat RI 1" in filtered.text
    assert "Kandidat RI 2" not in filtered.text
