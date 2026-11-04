from datetime import datetime
from collections.abc import Generator
from io import BytesIO
from pathlib import Path
import shutil
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.config import settings
from app.main import app
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app, base_url="http://localhost")
TEST_MAX_UPLOAD_SIZE = 100 * 1024 * 1024


@pytest.fixture(autouse=True)
def isolated_upload_storage(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    data_dir = Path(__file__).resolve().parent / f".test-data-{uuid4().hex}"
    assert not data_dir.exists()
    monkeypatch.setattr("app.services.workbook_storage.DATA_DIR", data_dir)
    monkeypatch.setattr(settings, "max_upload_size_bytes", TEST_MAX_UPLOAD_SIZE)
    yield
    if data_dir.exists():
        shutil.rmtree(data_dir)


def build_ri_workbook() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rincian Penerimaan Barang"
    sheet["B1"] = "PT OLI"

    _add_document(sheet, 5, "RI.OLI.2026.I.00001", datetime(2026, 1, 8), "SUPPLIER A")
    _add_detail_header(sheet, 7)
    _add_detail(sheet, 8, "ITEM-001", "Barang A", 1, None)
    _add_detail(sheet, 9, "ITEM-001", "Barang A", 2, "pcs")
    sheet["L10"] = 3
    _add_footer(sheet, 14, 1, 3)

    _add_document(sheet, 19, "RI.OLI.2026.I.00001", datetime(2026, 1, 8), "SUPPLIER A")
    _add_detail_header(sheet, 21)
    _add_detail(sheet, 22, "ITEM-002", "Barang B", 5, None)
    _add_footer(sheet, 26, 2, 4)

    _add_detail_header(sheet, 30)
    _add_detail(sheet, 31, "ITEM-CONT", "Continuation", 4, "pcs")
    _add_footer(sheet, 34, 3, 4)
    _add_detail(sheet, 37, "ITEM-NO-HEADER", "No table header", 6, "pcs")
    _add_footer(sheet, 40, 4, 4)

    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def build_many_ri_workbook(document_count: int) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rincian Penerimaan Barang"
    for index in range(document_count):
        header_row = 1 + index * 11
        _add_document(
            sheet,
            header_row,
            f"RI.OLI.2026.I.{index + 1:05d}",
            datetime(2026, 1, 8),
            "SUPPLIER A",
        )
        _add_detail_header(sheet, header_row + 2)
        _add_detail(sheet, header_row + 3, f"ITEM-{index + 1:03d}", "Barang", 1, "pcs")
        _add_footer(sheet, header_row + 8, index + 1, document_count)
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def _add_document(sheet, row: int, number: str, date_value: datetime, supplier: str) -> None:
    sheet.merge_cells(start_row=row, start_column=3, end_row=row, end_column=4)
    sheet.merge_cells(start_row=row, start_column=5, end_row=row, end_column=8)
    sheet.merge_cells(start_row=row, start_column=10, end_row=row, end_column=13)
    sheet.merge_cells(start_row=row, start_column=14, end_row=row, end_column=18)
    sheet.cell(row, 3, "Nomor #")
    sheet.cell(row, 5, number)
    sheet.cell(row, 10, "Pemasok")
    sheet.cell(row, 14, supplier)

    date_row = row + 1
    sheet.merge_cells(start_row=date_row, start_column=3, end_row=date_row, end_column=4)
    sheet.merge_cells(start_row=date_row, start_column=5, end_row=date_row, end_column=8)
    sheet.cell(date_row, 3, "Tanggal")
    sheet.cell(date_row, 5, date_value)


def _add_detail_header(sheet, row: int) -> None:
    for start, end, label in [
        (6, 7, "Kode #"),
        (8, 10, "Nama Barang"),
        (12, 14, "Kuantitas"),
        (16, 18, "Satuan"),
    ]:
        sheet.merge_cells(start_row=row, start_column=start, end_row=row, end_column=end)
        sheet.cell(row, start, label)


def _add_detail(sheet, row: int, code: str, name: str, quantity: int, unit: str | None) -> None:
    sheet.merge_cells(start_row=row, start_column=8, end_row=row, end_column=10)
    sheet.merge_cells(start_row=row, start_column=12, end_row=row, end_column=14)
    sheet["F" + str(row)] = code
    sheet["H" + str(row)] = name
    sheet["L" + str(row)] = quantity
    if unit is not None:
        sheet["P" + str(row)] = unit


def _add_footer(sheet, row: int, page: int, total_pages: int) -> None:
    sheet[f"B{row}"] = f"Halaman {page}"
    sheet[f"R{row}"] = f" dari {total_pages}"


def upload_ri_workbook(content: bytes | None = None):
    client.get("/workbooks")
    response = client.post(
        "/workbooks/upload",
        files=[
            (
                "files",
                (
                    "OLI_GRN_Rincian Penerimaan Barang_fixture.xlsx",
                    content or build_ri_workbook(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            )
        ],
        data={"csrf_token": client.cookies.get("solog_csrf", "")},
        headers={"Origin": "http://localhost"},
    )
    assert response.status_code == 201, response.text
    return WorkbookStorage().list_workbooks()[0]


def test_detector_keeps_duplicate_lines_and_marks_required_holds() -> None:
    record = upload_ri_workbook()
    analysis = WorkbookStorage().analyze_ri_layout(record)

    assert analysis.source_file_id == record.source_file_id
    assert analysis.worksheet.name == "Rincian Penerimaan Barang"
    assert analysis.summary.page_count == 4
    assert analysis.summary.candidate_document_count == 2
    assert analysis.summary.candidate_detail_count == 5
    assert analysis.summary.attached_detail_count == 3
    assert analysis.summary.unresolved_row_count == 3
    assert analysis.summary.pages_without_document_header == 2
    assert analysis.anomaly_counts["unit_missing"] == 2

    first, second = analysis.candidates
    assert first.header.document_number.normalized_value == "RI.OLI.2026.I.00001"
    assert first.header.date.raw_value == datetime(2026, 1, 8)
    assert first.header.supplier.raw_value == "SUPPLIER A"
    assert [detail.row_number for detail in first.details] == [8, 9]
    assert first.details[0].item_code.normalized_value == "ITEM-001"
    assert first.details[0].unit.raw_value is None
    assert first.details[0].status == "HOLD"
    assert first.details[1].item_code.normalized_value == "ITEM-001"
    assert first.details[1].status == "HOLD"
    assert "repeated_item_code" in first.details[1].anomaly_codes
    assert second.header.document_number.normalized_value == first.header.document_number.normalized_value
    assert first.status == second.status == "HOLD"
    assert all(
        anomaly.code == "repeated_document_number"
        for anomaly in analysis.anomalies
        if anomaly.code == "repeated_document_number"
    )


def test_detector_holds_headerless_continuation_and_quantity_only_row() -> None:
    record = upload_ri_workbook()
    analysis = WorkbookStorage().analyze_ri_layout(record)

    assert [row.reason_code for row in analysis.unresolved_rows] == [
        "quantity_only",
        "detail_without_document_header",
        "detail_without_document_header",
    ]
    assert analysis.unresolved_rows[0].row_number == 10
    assert analysis.unresolved_rows[0].fields["quantity"].raw_value == 3
    assert analysis.unresolved_rows[1].row_number == 31
    assert analysis.unresolved_rows[1].page_number == 3
    assert analysis.unresolved_rows[1].fields["item_code"].raw_value == "ITEM-CONT"
    assert analysis.unresolved_rows[2].row_number == 37
    assert 31 not in [detail.row_number for candidate in analysis.candidates for detail in candidate.details]
    assert 37 not in [detail.row_number for candidate in analysis.candidates for detail in candidate.details]
    assert sum(page.repeated_table_header_count for page in analysis.pages) == 3


def test_detector_uses_labels_merges_styles_and_physical_source_locators() -> None:
    record = upload_ri_workbook()
    analysis = WorkbookStorage().analyze_ri_layout(record)
    candidate = analysis.candidates[0]

    assert candidate.header.document_number.source_locator.source_file_id == record.source_file_id
    assert candidate.header.document_number.source_locator.sheet_name == "Rincian Penerimaan Barang"
    assert candidate.header.document_number.source_locator.cell_coordinate == "E5"
    assert candidate.header.document_number.source_locator.row_number == 5
    assert candidate.details[0].quantity.source_locator.cell_coordinate == "L8"
    number_evidence = next(
        evidence
        for evidence in candidate.detection_evidence
        if evidence.code == "document_number_value"
    )
    assert number_evidence.merged_range == "E5:H5"
    assert number_evidence.style_id is not None
    assert number_evidence.position_matched is True
    assert any(evidence.code == "detail_label_kode" for evidence in candidate.detection_evidence)
    assert candidate.header.document_number.normalized_value == "RI.OLI.2026.I.00001"
    assert candidate.header.date.normalized_value == datetime(2026, 1, 8)
    assert candidate.details[0].quantity.normalized_value == 1
    assert candidate.confidence == "HIGH"


def test_ri_preview_lists_candidates_holds_and_links_to_physical_preview() -> None:
    record = upload_ri_workbook()

    response = client.get(f"/workbooks/{record.source_file_id}/ri-candidates")

    assert response.status_code == 200, response.text
    assert "Kandidat ekstraksi RI" in response.text
    assert "Halaman tanpa header" in response.text
    assert "quantity_only" in response.text
    assert "repeated_document_number" in response.text
    assert f"/workbooks/{record.source_file_id}/sheets/1/preview?start_row=5" in response.text


def test_candidate_preview_paginates_documents_and_keeps_source_links() -> None:
    record = upload_ri_workbook(build_many_ri_workbook(21))

    response = client.get(
        f"/workbooks/{record.source_file_id}/ri-candidates?candidate_page=2"
    )

    assert response.status_code == 200, response.text
    assert "Kandidat 21" in response.text
    assert "2 / 2" in response.text
    assert "candidate_page=1" in response.text
    assert f"/workbooks/{record.source_file_id}/sheets/1/preview?start_row=221" in response.text


def test_analysis_does_not_modify_uploaded_workbook_bytes() -> None:
    content = build_ri_workbook()
    record = upload_ri_workbook(content)
    source_path = WorkbookStorage().upload_dir / record.storage_filename
    before = source_path.read_bytes()

    WorkbookStorage().analyze_ri_layout(record)

    assert source_path.read_bytes() == before == content


def test_candidate_analysis_rejects_missing_sheet_without_mutating_metadata() -> None:
    record = upload_ri_workbook()

    response = client.get(f"/workbooks/{record.source_file_id}/ri-candidates?sheet_index=2")

    assert response.status_code == 422
    assert "Worksheet yang diminta tidak ditemukan" in response.text
    assert WorkbookStorage().get_workbook(record.source_file_id).read_status == "readable"
