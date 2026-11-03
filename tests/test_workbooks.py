from copy import copy
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import shutil
import zipfile
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook
from openpyxl.worksheet.formula import ArrayFormula

from app.config import settings
from app.main import app
from app.services.workbook_storage import WorkbookStorage

client = TestClient(app)
TEST_MAX_UPLOAD_SIZE = 100 * 1024 * 1024


@pytest.fixture(autouse=True)
def isolated_upload_storage(monkeypatch: pytest.MonkeyPatch) -> None:
    data_dir = Path(__file__).resolve().parent / f".test-data-{uuid4().hex}"
    assert not data_dir.exists()
    monkeypatch.setattr("app.services.workbook_storage.DATA_DIR", data_dir)
    monkeypatch.setattr(settings, "max_upload_size_bytes", TEST_MAX_UPLOAD_SIZE)
    yield
    if data_dir.exists():
        shutil.rmtree(data_dir)


def build_workbook(*, include_second_sheet: bool = True) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    sheet["A1"] = "Example"
    sheet["A2"] = 42
    sheet["A2"].number_format = "0.00"
    sheet["A3"] = "=SUM(A2:A2)"
    formula_font = copy(sheet["A3"].font)
    formula_font.bold = True
    sheet["A3"].font = formula_font
    sheet.merge_cells("B2:C3")
    sheet["B2"] = "Merged value"

    if include_second_sheet:
        hidden = workbook.create_sheet("Hidden")
        hidden.sheet_state = "hidden"
        hidden["B7"] = "Physical row"
        hidden["C8"] = True
        hidden["D9"] = datetime(2026, 1, 2)
        hidden["E10"] = ArrayFormula(ref="E10:E11", text="=SUM(B7:B8)")

    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def build_paged_workbook() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Paged"
    sheet["A1"] = "First page"
    sheet["Z45"] = "Later page"

    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def upload_part(filename: str, content: bytes) -> tuple[str, tuple[str, bytes, str]]:
    return "files", (filename, content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def upload_one(content: bytes | None = None, filename: str = "source.xlsx"):
    return client.post(
        "/workbooks/upload",
        files=[upload_part(filename, content or build_workbook())],
    )


def test_upload_accepts_one_workbook_and_lists_readable_metadata() -> None:
    content = build_workbook()

    response = upload_one(content)

    assert response.status_code == 201, response.text
    assert "source.xlsx" in response.text
    assert sha256(content).hexdigest() in response.text
    assert "Siap dibaca" in response.text
    records = WorkbookStorage().list_workbooks()
    assert len(records) == 1
    assert records[0].size_bytes == len(content)


def test_upload_accepts_multiple_workbooks() -> None:
    response = client.post(
        "/workbooks/upload",
        files=[
            upload_part("one.xlsx", build_workbook()),
            upload_part("two.xlsx", build_workbook(include_second_sheet=False)),
        ],
    )

    assert response.status_code == 201, response.text
    assert len(WorkbookStorage().list_workbooks()) == 2
    assert "one.xlsx" in response.text
    assert "two.xlsx" in response.text


def test_upload_rejects_invalid_extension() -> None:
    response = upload_one(filename="source.xls")

    assert response.status_code == 207
    assert "Hanya berkas berekstensi .xlsx" in response.text
    assert WorkbookStorage().list_workbooks() == []


def test_upload_rejects_non_xlsx_content() -> None:
    response = upload_one(content=b"not an xlsx archive")

    assert response.status_code == 207
    assert "bukan paket XLSX/ZIP yang valid" in response.text
    assert WorkbookStorage().list_workbooks() == []


def test_upload_rejects_file_over_configured_size(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "max_upload_size_bytes", 10)

    response = upload_one(content=build_workbook())

    assert response.status_code == 207
    assert "melebihi batas" in response.text
    assert WorkbookStorage().list_workbooks() == []


def test_duplicate_original_filenames_get_unique_internal_names() -> None:
    content = build_workbook()
    response = client.post(
        "/workbooks/upload",
        files=[
            upload_part("duplicate.xlsx", content),
            upload_part("duplicate.xlsx", content),
        ],
    )

    records = WorkbookStorage().list_workbooks()
    assert response.status_code == 201, response.text
    assert len(records) == 2
    assert {record.source_filename for record in records} == {"duplicate.xlsx"}
    assert len({record.source_file_id for record in records}) == 2
    assert len({record.storage_filename for record in records}) == 2


def test_original_filename_cannot_control_storage_path() -> None:
    response = upload_one(filename="../../outside.xlsx")

    record = WorkbookStorage().list_workbooks()[0]
    assert response.status_code == 201
    assert record.source_filename == "../../outside.xlsx"
    assert record.storage_filename == f"{record.source_file_id}.xlsx"
    assert "/" not in record.storage_filename
    assert "\\" not in record.storage_filename


def test_cross_origin_upload_is_rejected() -> None:
    response = client.post(
        "/workbooks/upload",
        files=[upload_part("source.xlsx", build_workbook())],
        headers={"Origin": "https://attacker.example"},
    )

    assert response.status_code == 403
    assert "lintas-origin" in response.text
    assert WorkbookStorage().list_workbooks() == []


def test_same_origin_upload_is_allowed() -> None:
    response = client.post(
        "/workbooks/upload",
        files=[upload_part("source.xlsx", build_workbook())],
        headers={"Origin": "http://testserver"},
    )

    assert response.status_code == 201


def test_sha256_is_calculated_from_exact_uploaded_bytes() -> None:
    content = build_workbook()

    upload_one(content)

    assert WorkbookStorage().list_workbooks()[0].source_sha256 == sha256(content).hexdigest()


def test_reader_preserves_sheet_order_status_and_dimensions() -> None:
    response = upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    detail = WorkbookStorage().inspect(record.source_file_id)

    assert response.status_code == 201
    assert detail.worksheet_names == ["Data", "Hidden"]
    assert [sheet.sheet_index for sheet in detail.worksheets] == [1, 2]
    assert detail.worksheets[0].status == "visible"
    assert detail.worksheets[1].status == "hidden"
    assert detail.worksheets[0].max_row == 3
    assert detail.worksheets[0].max_column == 3


def test_reader_preserves_cell_values_and_types() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    cells = {
        cell.coordinate: cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[0].preview_cells
    }

    assert cells["A1"].value == "Example"
    assert cells["A1"].data_type == "s"
    assert cells["A2"].value == 42
    assert cells["A2"].data_type == "n"
    assert cells["A1"].row_number == 1
    assert cells["A1"].column_number == 1
    assert cells["C2"].value is None
    assert cells["C2"].is_empty is True


def test_reader_preserves_formula_without_computing_cached_result() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    formula_cell = next(
        cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[0].preview_cells
        if cell.coordinate == "A3"
    )

    assert formula_cell.value == "=SUM(A2:A2)"
    assert formula_cell.data_type == "f"
    assert formula_cell.formula == "=SUM(A2:A2)"


def test_reader_preserves_array_formula_and_its_range_metadata() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    formula_cell = next(
        cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[1].preview_cells
        if cell.coordinate == "E10"
    )

    assert formula_cell.formula == "=SUM(B7:B8)"
    assert formula_cell.formula_metadata == {"ref": "E10:E11", "text": "=SUM(B7:B8)"}


def test_reader_preserves_number_format_and_relevant_style() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    cell = next(
        cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[0].preview_cells
        if cell.coordinate == "A2"
    )

    assert cell.number_format == "0.00"
    assert cell.style.style_id > 0
    assert cell.style.font_bold is False


def test_reader_returns_merged_range_main_cell_and_members() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    merged = WorkbookStorage().inspect(record.source_file_id).worksheets[0].merged_ranges[0]

    assert merged.coordinate == "B2:C3"
    assert merged.main_cell_coordinate == "B2"
    assert merged.member_coordinates == ["C2", "B3", "C3"]


def test_source_locator_uses_physical_row_number() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    cell = next(
        cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[1].preview_cells
        if cell.coordinate == "B7"
    )

    assert cell.row_number == 7
    assert cell.source_locator.source_file_id == record.source_file_id
    assert cell.source_locator.source_filename == "source.xlsx"
    assert cell.source_locator.source_sha256 == record.source_sha256
    assert cell.source_locator.sheet_name == "Hidden"
    assert cell.source_locator.sheet_index == 2
    assert cell.source_locator.row_number == 7
    assert cell.source_locator.cell_coordinate == "B7"


def test_reader_preserves_boolean_and_date_values() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]

    cells = {
        cell.coordinate: cell
        for cell in WorkbookStorage().inspect(record.source_file_id).worksheets[1].preview_cells
    }

    assert cells["C8"].value is True
    assert cells["C8"].data_type == "b"
    assert cells["D9"].value == datetime(2026, 1, 2)
    assert cells["D9"].data_type == "d"


def test_source_bytes_are_unchanged_after_reading() -> None:
    original = build_workbook()
    upload_one(original)
    record = WorkbookStorage().list_workbooks()[0]
    stored_path = WorkbookStorage().upload_dir / record.storage_filename
    stored_before = stored_path.read_bytes()

    response = client.get(f"/workbooks/{record.source_file_id}")

    stored_after = stored_path.read_bytes()
    assert response.status_code == 200
    assert stored_before == original
    assert stored_after == original


def test_worksheet_preview_pages_rows_and_columns_with_physical_locator() -> None:
    upload_one(build_paged_workbook())
    record = WorkbookStorage().list_workbooks()[0]

    response = client.get(
        f"/workbooks/{record.source_file_id}/sheets/1/preview",
        params={"start_row": 41, "start_column": 21},
    )

    assert response.status_code == 200, response.text
    assert "Z45" in response.text
    assert "Later page" in response.text
    page = WorkbookStorage().read_sheet_page(
        record,
        sheet_index=1,
        start_row=41,
        start_column=21,
    )
    cell = next(cell for cell in page.cells if cell.coordinate == "Z45")
    assert cell.row_number == 45
    assert cell.column_number == 26
    assert cell.source_locator.row_number == 45
    assert cell.source_locator.cell_coordinate == "Z45"


def test_detail_preview_exposes_pagination_for_larger_worksheets() -> None:
    upload_one(build_paged_workbook())
    record = WorkbookStorage().list_workbooks()[0]

    response = client.get(f"/workbooks/{record.source_file_id}")

    assert response.status_code == 200, response.text
    assert "Baris berikutnya" in response.text
    assert "Kolom berikutnya" in response.text


def test_worksheet_preview_rejects_nonpositive_sheet_index() -> None:
    upload_one(build_paged_workbook())
    record = WorkbookStorage().list_workbooks()[0]

    response = client.get(f"/workbooks/{record.source_file_id}/sheets/0/preview")

    assert response.status_code == 422


def test_modified_stored_copy_is_not_read_and_status_is_updated() -> None:
    upload_one()
    record = WorkbookStorage().list_workbooks()[0]
    stored_path = WorkbookStorage().upload_dir / record.storage_filename
    stored_path.write_bytes(b"changed")

    response = client.get(f"/workbooks/{record.source_file_id}")

    updated = WorkbookStorage().get_workbook(record.source_file_id)
    assert response.status_code == 422
    assert "Hash workbook berubah" in response.text
    assert updated.read_status == "error"
    assert "Hash workbook berubah" in (updated.read_error or "")


def test_corrupt_zip_package_is_rejected() -> None:
    original = build_workbook()
    output = BytesIO()
    with zipfile.ZipFile(BytesIO(original), "r") as source:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for member in source.infolist():
                contents = (
                    b"<worksheet><broken></worksheet>"
                    if member.filename == "xl/worksheets/sheet1.xml"
                    else source.read(member.filename)
                )
                target.writestr(member.filename, contents)

    response = upload_one(content=output.getvalue())

    assert response.status_code == 207
    assert "rusak" in response.text or "tidak valid" in response.text, response.text
    assert WorkbookStorage().list_workbooks() == []


def test_suspicious_compression_ratio_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.services.xlsx_reader as xlsx_reader

    original = build_workbook()
    expanded = BytesIO()
    with zipfile.ZipFile(BytesIO(original), "r") as source:
        with zipfile.ZipFile(expanded, "w", compression=zipfile.ZIP_DEFLATED) as target:
            for member in source.infolist():
                target.writestr(member.filename, source.read(member.filename))
            target.writestr("suspicious.txt", b"A" * (1024 * 1024))
    monkeypatch.setattr(xlsx_reader, "MAX_COMPRESSION_RATIO", 100)

    response = upload_one(content=expanded.getvalue())

    assert response.status_code == 207
    assert "Rasio kompresi XLSX mencurigakan" in response.text
    assert WorkbookStorage().list_workbooks() == []
