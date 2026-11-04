from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pymysql
from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app
from app.models.mapping import MappingStatus
from app.services.master_data_mapping import (
    MASTER_MAPPINGS_PER_PAGE,
    build_master_data_mapping_profile,
    paginate_master_data_mappings,
    validate_master_data_mapping_profile,
)
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app, base_url="http://localhost")


def build_pr_workbook(item_count: int = 2) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rincian Permintaan Barang"
    sheet["F7"] = "Kode #"
    sheet["H7"] = "Nama Barang"
    for row_number in range(8, 8 + item_count):
        sheet.cell(row_number, 6, "ITEM-01")
        sheet.cell(row_number, 8, f"Barang {row_number}")
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def build_grn_workbook(*, blank_unit: bool = True, conflicting_item: bool = True) -> bytes:
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
    sheet["F8"] = "ITEM-01"
    sheet["H8"] = "Nama Awal"
    sheet["L8"] = 2
    if not blank_unit:
        sheet["P8"] = "PCS"
    sheet["F9"] = "ITEM-01"
    sheet["H9"] = "Nama Berbeda" if conflicting_item else "Nama Awal"
    sheet["L9"] = 3
    if not blank_unit:
        sheet["P9"] = "PCS"
    sheet["B10"] = "Halaman 1"
    sheet["F11"] = "ITEM-02"
    sheet["H11"] = "Detail tanpa header dokumen"
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def upload_workbook(
    monkeypatch,
    tmp_path: Path,
    filename: str,
    content: bytes,
) -> tuple[object, Path]:
    import app.services.workbook_storage as workbook_storage_module

    data_dir = tmp_path / "master-mapping"
    monkeypatch.setattr(workbook_storage_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(workbook_storage_module, "PROJECT_ROOT", tmp_path)
    client.get("/workbooks")
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    filename,
                    content,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": "http://localhost"},
    )
    assert response.status_code == 201, response.text
    record = next(
        record
        for record in WorkbookStorage().list_workbooks()
        if record.source_filename == filename
    )
    return record, data_dir


def test_profile_preserves_hash_locator_and_crosswalk_without_target_ids(
    monkeypatch, tmp_path: Path
) -> None:
    pr_bytes = build_pr_workbook()
    grn_bytes = build_grn_workbook(blank_unit=True)
    pr_record, _ = upload_workbook(
        monkeypatch, tmp_path, "OLI_PR_fixture.xlsx", pr_bytes
    )
    upload_workbook(monkeypatch, tmp_path, "OLI_GRN_fixture.xlsx", grn_bytes)

    profile = build_master_data_mapping_profile()

    item_code = next(
        candidate
        for candidate in profile.candidates
        if candidate.source_file_id == pr_record.source_file_id
        and candidate.source_field == "item_code"
    )
    assert item_code.source_sha256 == sha256(pr_bytes).hexdigest()
    assert item_code.source_value == "ITEM-01"
    assert item_code.source_locator.sheet_name == "Rincian Permintaan Barang"
    assert item_code.source_locator.cell_coordinate == "F8"
    assert item_code.source_fingerprint
    assert item_code.candidate_target_id is None
    assert item_code.candidate_target_table == "items"
    assert item_code.mapping_status == MappingStatus.REVIEW_REQUIRED
    assert all(
        candidate.mapping_status == MappingStatus.REVIEW_REQUIRED
        for candidate in profile.candidates
    )
    unit = next(
        candidate for candidate in profile.candidates if candidate.source_entity == "unit"
    )
    assert unit.target_evidence == "HISTORICAL_SCHEMA_ONLY"
    assert "bertentangan" in unit.target_evidence_note
    assert profile.relationship_status == "UNKNOWN"
    assert profile.summary.target_schema_status == "UNKNOWN"


def test_blank_values_duplicates_and_conflicting_keys_are_reported_without_merging(
    monkeypatch, tmp_path: Path
) -> None:
    upload_workbook(
        monkeypatch,
        tmp_path,
        "OLI_GRN_quality.xlsx",
        build_grn_workbook(blank_unit=True, conflicting_item=True),
    )

    profile = build_master_data_mapping_profile()
    item_codes = [
        candidate
        for candidate in profile.candidates
        if candidate.source_entity == "item" and candidate.source_field == "item_code"
    ]
    item_names = [
        candidate
        for candidate in profile.candidates
        if candidate.source_entity == "item" and candidate.source_field == "item_name"
    ]
    units = [candidate for candidate in profile.candidates if candidate.source_entity == "unit"]

    assert len(item_codes) == 3
    assert len(item_names) == 3
    assert sum(candidate.duplicate_candidate for candidate in item_codes) == 2
    assert sum(candidate.conflicting_natural_key for candidate in item_codes) == 2
    assert item_codes[-1].source_locator.cell_coordinate == "F11"
    assert item_codes[-1].source_evidence_confidence == "LOW"
    assert len(units) == 3
    assert all(candidate.missing_value for candidate in units)
    assert all(
        candidate.source_locator.cell_coordinate in {"P8", "P9", "P11"}
        for candidate in units
    )
    assert all(candidate.mapping_status == MappingStatus.REVIEW_REQUIRED for candidate in profile.candidates)


def test_identical_uploads_remain_separate_crosswalk_occurrences(
    monkeypatch, tmp_path: Path
) -> None:
    content = build_grn_workbook(blank_unit=False, conflicting_item=False)
    first, _ = upload_workbook(monkeypatch, tmp_path, "OLI_GRN_first.xlsx", content)
    second, _ = upload_workbook(monkeypatch, tmp_path, "OLI_GRN_second.xlsx", content)

    profile = build_master_data_mapping_profile()
    first_rows = [
        candidate
        for candidate in profile.candidates
        if candidate.source_file_id == first.source_file_id
    ]
    second_rows = [
        candidate
        for candidate in profile.candidates
        if candidate.source_file_id == second.source_file_id
    ]

    assert first.source_sha256 == second.source_sha256
    assert first_rows and second_rows
    assert {row.source_locator.source_file_id for row in first_rows} == {first.source_file_id}
    assert {row.source_locator.source_file_id for row in second_rows} == {second.source_file_id}
    assert {row.mapping_id for row in first_rows}.isdisjoint(
        {row.mapping_id for row in second_rows}
    )
    assert profile.summary.source_workbook_count == 2
    assert profile.summary.distinct_workbook_sha256_count == 1


def test_profile_validation_rejects_changed_source_hash(
    monkeypatch, tmp_path: Path
) -> None:
    record, _ = upload_workbook(
        monkeypatch,
        tmp_path,
        "OLI_PR_hash.xlsx",
        build_pr_workbook(item_count=1),
    )
    profile = build_master_data_mapping_profile()
    source = profile.source_workbooks[0].model_copy(
        update={"source_sha256": "0" * 64}
    )
    invalid_profile = profile.model_copy(update={"source_workbooks": [source]})

    try:
        validate_master_data_mapping_profile(invalid_profile, [record])
    except ValueError as exc:
        assert "hash" in str(exc).casefold()
    else:
        raise AssertionError("Perubahan SHA-256 harus menginvalidasi profil.")


def test_pagination_and_status_filter_are_applied() -> None:
    from app.models.master_data_mapping import (
        MasterDataMappingCandidate,
        MasterDataMappingProfile,
        MasterDataMappingSummary,
        MasterSourceWorkbook,
    )
    from app.models.workbook import SourceLocator

    source_id = "a" * 32
    source_hash = "b" * 64
    source_name = "OLI_PR_fixture.xlsx"
    source = MasterSourceWorkbook(
        source_file_id=source_id,
        source_filename=source_name,
        source_sha256=source_hash,
        worksheet_name="Rincian Permintaan Barang",
        worksheet_index=1,
        master_observation_count=MASTER_MAPPINGS_PER_PAGE + 1,
    )
    candidates = [
        MasterDataMappingCandidate(
            mapping_id=f"mapping-{index}",
            source_entity="item",
            source_file_id=source_id,
            source_filename=source_name,
            source_sha256=source_hash,
            source_sheet=source.worksheet_name,
            source_sheet_index=1,
            source_field="item_code",
            source_header="Kode #",
            source_value=f"ITEM-{index}",
            source_data_type="s",
            source_locator=SourceLocator(
                source_file_id=source_id,
                source_filename=source_name,
                source_sha256=source_hash,
                sheet_name=source.worksheet_name,
                sheet_index=1,
                row_number=index + 1,
                cell_coordinate=f"F{index + 1}",
            ),
            source_fingerprint=f"{index:064x}",
            candidate_target_table="items",
            candidate_target_column="code",
            target_evidence="HISTORICAL_SCHEMA_ONLY",
            target_evidence_note="Reference only",
            transformation_proposal="Tidak dijalankan.",
            natural_key_proposal="Kandidat saja.",
            null_handling_proposal="UNKNOWN.",
            duplicate_handling_proposal="Tidak digabung.",
            source_evidence_confidence="HIGH",
        )
        for index in range(MASTER_MAPPINGS_PER_PAGE + 1)
    ]
    profile = MasterDataMappingProfile(
        source_workbooks=[source],
        candidates=candidates,
        summary=MasterDataMappingSummary(
            source_workbook_count=1,
            distinct_workbook_sha256_count=1,
            candidate_count=len(candidates),
            supplier_candidate_count=0,
            item_candidate_count=len(candidates),
            unit_candidate_count=0,
            missing_value_count=0,
            duplicate_candidate_count=0,
            conflicting_natural_key_count=0,
            mapping_status_counts={"REVIEW_REQUIRED": len(candidates)},
        ),
        relationship_note="UNKNOWN",
    )

    second_page = paginate_master_data_mappings(
        profile,
        page=2,
        entity_filter="item",
        status_filter="REVIEW_REQUIRED",
    )
    empty_approved = paginate_master_data_mappings(
        profile,
        entity_filter="item",
        status_filter="APPROVED",
    )

    assert second_page.page == 2
    assert second_page.total_pages == 2
    assert len(second_page.candidates) == 1
    assert empty_approved.total_filtered == 0


def test_master_mapping_page_has_no_mutation_endpoint_and_uses_no_database(
    monkeypatch, tmp_path: Path
) -> None:
    upload_workbook(
        monkeypatch,
        tmp_path,
        "OLI_PR_ui.xlsx",
        build_pr_workbook(item_count=14),
    )
    def reject_database_connection(*arguments, **keywords):
        raise AssertionError(
            "Stage 4.4.3 must not connect to a database "
            f"({len(arguments)} positional, {len(keywords)} keyword arguments)."
        )

    monkeypatch.setattr(pymysql, "connect", reject_database_connection)

    response = client.get(
        "/master-data-mappings?entity=item&status=REVIEW_REQUIRED&page=2"
    )
    assert response.status_code == 200
    assert "REVIEW_REQUIRED" in response.text
    assert "items.code" in response.text
    assert "/workbooks/" in response.text
    assert "start_row=" in response.text
    assert client.post("/master-data-mappings").status_code == 405


def test_analysis_does_not_change_uploaded_workbook_bytes(
    monkeypatch, tmp_path: Path
) -> None:
    content = build_grn_workbook(blank_unit=True)
    record, data_dir = upload_workbook(
        monkeypatch, tmp_path, "OLI_GRN_immutable.xlsx", content
    )
    stored_path = data_dir / "uploads" / record.storage_filename
    before = stored_path.read_bytes()

    build_master_data_mapping_profile()

    assert stored_path.read_bytes() == before == content
