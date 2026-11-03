from pathlib import Path, PurePosixPath
import re
import zipfile
from xml.etree.ElementTree import ParseError

from defusedxml.ElementTree import iterparse, parse
from defusedxml.common import DefusedXmlException
from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.styles.colors import Color
from openpyxl.utils.cell import get_column_letter, range_boundaries
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import ValidationError

from app.models.workbook import (
    CellInfo,
    CellStyleInfo,
    MergedRangeInfo,
    SourceLocator,
    WorkbookDetail,
    WorkbookRecord,
    WorksheetPage,
    WorksheetInfo,
)

MAX_ARCHIVE_MEMBERS = 4096
MAX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
MAX_WORKBOOK_CELLS = 1_000_000
MAX_MERGED_RANGE_CELLS = 1_000_000
PREVIEW_MAX_ROWS = 20
PREVIEW_MAX_COLUMNS = 20

_WORKSHEET_XML_NAME = re.compile(r"^xl/worksheets/[^/]+\.xml$")
_REQUIRED_XLSX_PARTS = {
    "[Content_Types].xml",
    "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels",
}


class WorkbookReadError(Exception):
    """Raised when an uploaded file is not a safe, readable XLSX workbook."""


def validate_xlsx_package(path: Path) -> None:
    if not zipfile.is_zipfile(path):
        raise WorkbookReadError("Berkas bukan paket XLSX/ZIP yang valid.")

    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > MAX_ARCHIVE_MEMBERS:
                raise WorkbookReadError("Paket XLSX memiliki terlalu banyak bagian.")

            names = [member.filename for member in members]
            if len(names) != len(set(names)):
                raise WorkbookReadError("Paket XLSX memiliki nama bagian duplikat.")
            if not _REQUIRED_XLSX_PARTS.issubset(names):
                raise WorkbookReadError("Struktur paket XLSX tidak lengkap.")
            if "xl/vbaProject.bin" in names:
                raise WorkbookReadError("Workbook berisi macro; hanya XLSX tanpa macro yang didukung.")

            total_uncompressed = 0
            worksheet_parts: list[zipfile.ZipInfo] = []
            for member in members:
                member_path = PurePosixPath(member.filename)
                if (
                    member_path.is_absolute()
                    or "\\" in member.filename
                    or ".." in member_path.parts
                ):
                    raise WorkbookReadError("Paket XLSX berisi path bagian yang mencurigakan.")
                if member.flag_bits & 0x1:
                    raise WorkbookReadError("Paket XLSX terenkripsi tidak didukung.")

                total_uncompressed += member.file_size
                if total_uncompressed > MAX_UNCOMPRESSED_BYTES:
                    raise WorkbookReadError("Ukuran hasil ekstraksi XLSX melebihi batas aman.")
                if member.file_size and member.file_size / max(member.compress_size, 1) > MAX_COMPRESSION_RATIO:
                    raise WorkbookReadError("Rasio kompresi XLSX mencurigakan.")

                if _WORKSHEET_XML_NAME.fullmatch(member.filename):
                    worksheet_parts.append(member)

            if not worksheet_parts:
                raise WorkbookReadError("Paket XLSX tidak berisi worksheet.")

            if archive.testzip() is not None:
                raise WorkbookReadError("Paket XLSX rusak (CRC tidak cocok).")

            _validate_content_types(archive)
            _validate_worksheet_xml(archive, worksheet_parts)
    except WorkbookReadError:
        raise
    except (
        DefusedXmlException,
        OSError,
        ParseError,
        RuntimeError,
        TypeError,
        ValueError,
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
    ) as exc:
        raise WorkbookReadError("Paket XLSX rusak atau tidak dapat dibaca.") from exc


def _validate_content_types(archive: zipfile.ZipFile) -> None:
    with archive.open("[Content_Types].xml") as stream:
        root = parse(stream).getroot()
    workbook_type = next(
        (
            element.attrib.get("ContentType")
            for element in root
            if element.tag.rsplit("}", 1)[-1] == "Override"
            and element.attrib.get("PartName") == "/xl/workbook.xml"
        ),
        None,
    )
    if workbook_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml":
        raise WorkbookReadError("Tipe konten workbook bukan XLSX standar.")


def inspect_workbook(path: Path, source: WorkbookRecord) -> WorkbookDetail:
    validate_xlsx_package(path)
    workbook = None
    try:
        workbook = load_workbook(path, data_only=False, read_only=False)
        worksheet_infos = [
            _worksheet_info(worksheet, index, source)
            for index, worksheet in enumerate(workbook.worksheets, start=1)
        ]
    except WorkbookReadError:
        raise
    except (
        InvalidFileException,
        OSError,
        ParseError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        ValidationError,
        zipfile.BadZipFile,
        DefusedXmlException,
    ) as exc:
        raise WorkbookReadError("Workbook XLSX rusak atau struktur internalnya tidak valid.") from exc
    finally:
        if workbook is not None:
            workbook.close()

    if not worksheet_infos:
        raise WorkbookReadError("Workbook tidak memiliki worksheet.")

    return WorkbookDetail(
        source=source,
        worksheet_names=[sheet.name for sheet in worksheet_infos],
        worksheets=worksheet_infos,
    )


def read_worksheet_page(
    path: Path,
    source: WorkbookRecord,
    sheet_index: int,
    start_row: int = 1,
    start_column: int = 1,
) -> WorksheetPage:
    validate_xlsx_package(path)
    if sheet_index < 1 or start_row < 1 or start_column < 1:
        raise ValueError("Worksheet index and page coordinates must be positive.")

    workbook = None
    try:
        workbook = load_workbook(path, data_only=False, read_only=False)
        worksheet = workbook.worksheets[sheet_index - 1]
        cells = _worksheet_page_cells(
            worksheet,
            sheet_index,
            source,
            start_row,
            start_column,
        )
        return WorksheetPage(
            name=worksheet.title,
            sheet_index=sheet_index,
            max_row=worksheet.max_row,
            max_column=worksheet.max_column,
            cells=cells,
        )
    except IndexError as exc:
        raise WorkbookReadError("Worksheet yang diminta tidak ditemukan.") from exc
    except WorkbookReadError:
        raise
    except (
        InvalidFileException,
        OSError,
        ParseError,
        ValueError,
        TypeError,
        KeyError,
        ValidationError,
        zipfile.BadZipFile,
        DefusedXmlException,
    ) as exc:
        raise WorkbookReadError("Workbook XLSX rusak atau struktur internalnya tidak valid.") from exc
    finally:
        if workbook is not None:
            workbook.close()


def _validate_worksheet_xml(
    archive: zipfile.ZipFile,
    worksheet_parts: list[zipfile.ZipInfo],
) -> None:
    total_cells = 0
    total_merged_cells = 0
    try:
        for part in worksheet_parts:
            with archive.open(part) as stream:
                for _, element in iterparse(stream, events=("end",)):
                    local_name = element.tag.rsplit("}", 1)[-1]
                    if local_name == "c":
                        total_cells += 1
                        if total_cells > MAX_WORKBOOK_CELLS:
                            raise WorkbookReadError("Workbook memiliki terlalu banyak cell.")
                    elif local_name == "mergeCell":
                        merged_ref = element.attrib.get("ref")
                        if merged_ref:
                            min_col, min_row, max_col, max_row = range_boundaries(merged_ref)
                            total_merged_cells += (max_col - min_col + 1) * (max_row - min_row + 1)
                            if total_merged_cells > MAX_MERGED_RANGE_CELLS:
                                raise WorkbookReadError("Merged ranges workbook melebihi batas aman.")
                    element.clear()
    except WorkbookReadError:
        raise
    except (
        DefusedXmlException,
        ParseError,
        OSError,
        TypeError,
        ValueError,
        zipfile.BadZipFile,
    ) as exc:
        raise WorkbookReadError("XML worksheet rusak atau berisi struktur yang tidak aman.") from exc


def _worksheet_info(
    worksheet: Worksheet,
    sheet_index: int,
    source: WorkbookRecord,
) -> WorksheetInfo:
    status = worksheet.sheet_state
    preview_cells = _worksheet_page_cells(worksheet, sheet_index, source, 1, 1)
    merged_ranges = [
        _merged_range_info(merged_range.coord)
        for merged_range in worksheet.merged_cells.ranges
    ]

    return WorksheetInfo(
        name=worksheet.title,
        sheet_index=sheet_index,
        status=status,
        max_row=worksheet.max_row,
        max_column=worksheet.max_column,
        dimensions=worksheet.calculate_dimension(),
        preview_cells=preview_cells,
        merged_ranges=merged_ranges,
    )


def _worksheet_page_cells(
    worksheet: Worksheet,
    sheet_index: int,
    source: WorkbookRecord,
    start_row: int,
    start_column: int,
) -> list[CellInfo]:
    end_row = min(start_row + PREVIEW_MAX_ROWS - 1, worksheet.max_row)
    end_column = min(start_column + PREVIEW_MAX_COLUMNS - 1, worksheet.max_column)
    if start_row > end_row or start_column > end_column:
        return []

    cells: list[CellInfo] = []
    for row in worksheet.iter_rows(
        min_row=start_row,
        max_row=end_row,
        min_col=start_column,
        max_col=end_column,
    ):
        cells.extend(
            _cell_info(cell, worksheet.title, sheet_index, source)
            for cell in row
        )
    return cells


def _cell_info(
    cell: Cell,
    sheet_name: str,
    sheet_index: int,
    source: WorkbookRecord,
) -> CellInfo:
    value = cell.value
    formula = None
    formula_metadata = None
    if cell.data_type == "f":
        if isinstance(value, str):
            formula = value
        else:
            attributes = vars(value)
            if not all(
                item is None or isinstance(item, (str, int, float, bool))
                for item in attributes.values()
            ):
                raise WorkbookReadError("Workbook berisi tipe formula yang tidak didukung.")
            formula_metadata = attributes
            formula = attributes.get("text")
            value = {"formula": formula, **attributes}

    return CellInfo(
        coordinate=cell.coordinate,
        row_number=cell.row,
        column_number=cell.column,
        value=value,
        data_type=cell.data_type,
        formula=formula,
        formula_metadata=formula_metadata,
        number_format=cell.number_format,
        style=_cell_style(cell),
        is_empty=value is None or value == "",
        source_locator=SourceLocator(
            source_file_id=source.source_file_id,
            source_filename=source.source_filename,
            source_sha256=source.source_sha256,
            sheet_name=sheet_name,
            sheet_index=sheet_index,
            row_number=cell.row,
            cell_coordinate=cell.coordinate,
        ),
    )


def _cell_style(cell: Cell) -> CellStyleInfo:
    font = cell.font
    fill = cell.fill
    alignment = cell.alignment
    border_sides = [
        side_name
        for side_name in ("left", "right", "top", "bottom", "diagonal")
        if getattr(cell.border, side_name).style is not None
    ]
    return CellStyleInfo(
        style_id=cell.style_id,
        font_name=font.name,
        font_size=font.sz,
        font_bold=font.bold,
        font_italic=font.italic,
        font_color=_color_value(font.color),
        fill_type=fill.fill_type,
        fill_color=_color_value(fill.fgColor),
        horizontal_alignment=alignment.horizontal,
        vertical_alignment=alignment.vertical,
        wrap_text=bool(alignment.wrap_text),
        border_sides=border_sides,
    )


def _color_value(color: Color | None) -> str | None:
    if color is None:
        return None
    if color.type == "rgb":
        return color.rgb
    if color.type == "theme":
        return f"theme:{color.theme}"
    if color.type == "indexed":
        return f"indexed:{color.indexed}"
    return None


def _merged_range_info(coordinate: str) -> MergedRangeInfo:
    min_col, min_row, max_col, max_row = range_boundaries(coordinate)
    main_coordinate = f"{get_column_letter(min_col)}{min_row}"
    members = [
        f"{get_column_letter(column)}{row}"
        for row in range(min_row, max_row + 1)
        for column in range(min_col, max_col + 1)
        if (row, column) != (min_row, min_col)
    ]
    return MergedRangeInfo(
        coordinate=coordinate,
        main_cell_coordinate=main_coordinate,
        member_coordinates=members,
    )
