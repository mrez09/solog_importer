from collections import defaultdict
from pathlib import Path
import re
import zipfile
from xml.etree.ElementTree import ParseError

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import get_column_letter
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet
from defusedxml.common import DefusedXmlException
from pydantic import ValidationError

from app.models.ri_candidate import (
    CandidateValue,
    DetectionEvidence,
    PageLayoutSummary,
    RIAnalysisResult,
    RIAnalysisSummary,
    RIAnomaly,
    RIDetailCandidate,
    RIHeaderCandidate,
    RIRecordCandidate,
    UnresolvedRow,
    WorksheetLayoutMetadata,
)
from app.models.workbook import CellValue, SourceLocator, WorkbookRecord
from app.services.xlsx_reader import WorkbookReadError, validate_xlsx_package

_MIN_COLUMNS = 20
_PAGE_PATTERN = re.compile(r"^\s*halaman\s+(\d+)\s*$", re.IGNORECASE)
_HEADER_LABELS = {
    "Nomor #": 3,
    "Tanggal": 3,
    "Pemasok": 10,
}
_DETAIL_LABELS = {
    "Kode #": 6,
    "Nama Barang": 8,
    "Kuantitas": 12,
    "Satuan": 16,
}
_FIELD_COLUMNS = {
    "document_number": 5,
    "date": 5,
    "supplier": 14,
    "item_code": 6,
    "item_name": 8,
    "quantity": 12,
    "unit": 16,
}


def detect_ri_layout(
    path: Path,
    source: WorkbookRecord,
    sheet_index: int = 1,
) -> RIAnalysisResult:
    validate_xlsx_package(path)
    if sheet_index < 1:
        raise ValueError("Worksheet index must be positive.")

    workbook = None
    try:
        workbook = load_workbook(path, data_only=False, read_only=False)
        worksheet = workbook.worksheets[sheet_index - 1]
        result = _detect_worksheet(worksheet, source, sheet_index)
    except IndexError as exc:
        raise WorkbookReadError("Worksheet yang diminta tidak ditemukan.") from exc
    except WorkbookReadError:
        raise
    except (
        InvalidFileException,
        OSError,
        ParseError,
        TypeError,
        ValueError,
        KeyError,
        ValidationError,
        zipfile.BadZipFile,
        DefusedXmlException,
    ) as exc:
        raise WorkbookReadError("Layout worksheet tidak dapat dianalisis.") from exc
    finally:
        if workbook is not None:
            workbook.close()
    return result


def _detect_worksheet(
    worksheet: Worksheet,
    source: WorkbookRecord,
    sheet_index: int,
) -> RIAnalysisResult:
    merged_ranges = _merged_ranges_by_row(worksheet)
    max_column = max(worksheet.max_column, _MIN_COLUMNS)
    candidates: list[RIRecordCandidate] = []
    unresolved_rows: list[UnresolvedRow] = []
    anomalies: list[RIAnomaly] = []
    page_summaries: list[PageLayoutSummary] = []
    page_number = 1
    page_start_row = 1
    page_header_count = 0
    page_table_header_count = 0
    page_detail_count = 0
    page_unresolved_count = 0
    page_anomaly_count = 0
    page_has_content = False
    active_candidate: RIRecordCandidate | None = None
    table_header_active = False

    def locator(row_number: int, column_number: int) -> SourceLocator:
        return SourceLocator(
            source_file_id=source.source_file_id,
            source_filename=source.source_filename,
            source_sha256=source.source_sha256,
            sheet_name=worksheet.title,
            sheet_index=sheet_index,
            row_number=row_number,
            cell_coordinate=f"{get_column_letter(column_number)}{row_number}",
        )

    def merged_range(row_number: int, column_number: int) -> str | None:
        for min_column, max_column, coordinate in merged_ranges.get(row_number, []):
            if min_column <= column_number <= max_column:
                return coordinate
        return None

    def add_anomaly(
        code: str,
        title: str,
        reason: str,
        row_number: int,
        columns: list[int],
        candidate: RIRecordCandidate | None = None,
    ) -> None:
        nonlocal page_anomaly_count
        page_anomaly_count += 1
        anomaly = RIAnomaly(
            code=code,
            title=title,
            reason=reason,
            page_number=page_number,
            candidate_index=candidate.candidate_index if candidate else None,
            source_locators=[locator(row_number, column) for column in columns],
        )
        anomalies.append(anomaly)
        if candidate is not None:
            candidate.status = "HOLD"
            if code not in candidate.anomaly_codes:
                candidate.anomaly_codes.append(code)

    def evidence(
        code: str,
        description: str,
        cell: Cell,
        expected_column: int | None = None,
    ) -> DetectionEvidence:
        return DetectionEvidence(
            code=code,
            description=description,
            locator=locator(cell.row, cell.column),
            observed_value=cell.value,
            style_id=cell.style_id,
            merged_range=merged_range(cell.row, cell.column),
            expected_column=expected_column,
            position_matched=(
                cell.column == expected_column if expected_column is not None else None
            ),
        )

    def field_value(
        cell: Cell,
        field_name: str,
        *,
        label_confirmed: bool = True,
    ) -> CandidateValue:
        raw_value = cell.value
        is_empty = raw_value is None or raw_value == ""
        normalized_value = _normalize_value(field_name, raw_value)
        status = "PRESENT" if not is_empty and label_confirmed else "UNRESOLVED"
        return CandidateValue(
            raw_value=raw_value,
            normalized_value=normalized_value,
            data_type=cell.data_type,
            status=status,
            source_locator=locator(cell.row, cell.column),
        )

    def empty_field() -> CandidateValue:
        return CandidateValue(
            raw_value=None,
            normalized_value=None,
            data_type="n",
            status="UNRESOLVED",
            source_locator=None,
        )

    def close_page(end_row: int, footer: Cell | None = None) -> None:
        nonlocal page_number, page_start_row, page_header_count
        nonlocal page_table_header_count, page_detail_count, page_unresolved_count
        nonlocal page_anomaly_count
        nonlocal page_has_content, active_candidate, table_header_active
        page_end_number = page_number
        if footer is not None:
            page_match = _PAGE_PATTERN.match(str(footer.value or ""))
            if page_match:
                page_end_number = int(page_match.group(1))
        if page_has_content or footer is not None:
            page_summaries.append(
                PageLayoutSummary(
                    page_number=page_end_number,
                    start_row=page_start_row,
                    end_row=end_row,
                    document_header_count=page_header_count,
                    repeated_table_header_count=page_table_header_count,
                    detail_candidate_count=page_detail_count,
                    unresolved_row_count=page_unresolved_count,
                    status=(
                        "HOLD"
                        if page_anomaly_count > 0
                        else "CANDIDATE"
                    ),
                    footer_locator=(
                        locator(footer.row, footer.column) if footer is not None else None
                    ),
                )
            )
        page_number = (page_end_number + 1) if footer is not None else page_number
        page_start_row = end_row + 1
        page_header_count = 0
        page_table_header_count = 0
        page_detail_count = 0
        page_unresolved_count = 0
        page_anomaly_count = 0
        page_has_content = False
        active_candidate = None
        table_header_active = False

    for row_number, row_cells in enumerate(
        worksheet.iter_rows(
            min_row=1,
            max_row=worksheet.max_row,
            min_col=1,
            max_col=max_column,
        ),
        start=1,
    ):
        row_labels = _row_labels(row_cells)
        footer_cell = _page_footer_cell(row_cells)
        if footer_cell is not None:
            if active_candidate is not None:
                active_candidate.end_row = row_number
            if page_header_count == 0 and page_unresolved_count:
                add_anomaly(
                    "headerless_page",
                    "Halaman tanpa header RI",
                    "Baris detail pada halaman ini tidak memiliki header RI yang dapat dipastikan.",
                    row_number,
                    [footer_cell.column],
                )
            close_page(row_number, footer_cell)
            continue

        if not any(cell.value is not None and cell.value != "" for cell in row_cells):
            continue
        page_has_content = True

        number_label = row_labels.get("Nomor #")
        if number_label is not None:
            if active_candidate is not None:
                active_candidate.end_row = row_number - 1
            number_label_matched = number_label.column == _HEADER_LABELS["Nomor #"]
            supplier_label = row_labels.get("Pemasok")
            supplier_label_matched = (
                supplier_label is not None
                and supplier_label.column == _HEADER_LABELS["Pemasok"]
            )
            number_cell = row_cells[_FIELD_COLUMNS["document_number"] - 1]
            supplier_cell = row_cells[_FIELD_COLUMNS["supplier"] - 1]
            candidate_index = len(candidates) + 1
            header = RIHeaderCandidate(
                document_number=field_value(
                    number_cell,
                    "document_number",
                    label_confirmed=number_label_matched,
                ),
                date=empty_field(),
                supplier=field_value(
                    supplier_cell,
                    "supplier",
                    label_confirmed=supplier_label_matched,
                ),
            )
            confidence = "HIGH" if number_label_matched and supplier_label_matched else "LOW"
            new_candidate = RIRecordCandidate(
                candidate_index=candidate_index,
                header_row=row_number,
                end_row=row_number,
                page_numbers=[page_number],
                header=header,
                confidence=confidence,
                status="CANDIDATE_REVIEW",
                detection_evidence=[
                    evidence("document_number_label", "Label Nomor RI", number_label, 3),
                    evidence(
                        "document_number_value",
                        "Cell nilai Nomor RI berdasarkan label",
                        number_cell,
                        5,
                    ),
                ],
            )
            if supplier_label is not None:
                new_candidate.detection_evidence.extend(
                    [
                        evidence("supplier_label", "Label pemasok", supplier_label, 10),
                        evidence(
                            "supplier_value",
                            "Cell nilai pemasok berdasarkan label",
                            supplier_cell,
                            14,
                        ),
                    ]
                )
            candidates.append(new_candidate)
            active_candidate = new_candidate
            table_header_active = False
            page_header_count += 1
            if not number_label_matched:
                add_anomaly(
                    "misplaced_document_label",
                    "Label nomor RI tidak berada pada posisi pola",
                    "Label terdeteksi, tetapi tidak berada di kolom C seperti pola yang dianalisis.",
                    row_number,
                    [number_label.column, number_cell.column],
                    new_candidate,
                )
            if supplier_label is None or not supplier_label_matched:
                add_anomaly(
                    "supplier_label_unconfirmed",
                    "Label pemasok tidak terkonfirmasi",
                    "Nilai kolom N tidak dinyatakan sebagai pemasok oleh label pada posisi pola.",
                    row_number,
                    [supplier_cell.column],
                    new_candidate,
                )
            if header.document_number.status == "UNRESOLVED":
                add_anomaly(
                    "document_number_unresolved",
                    "Nomor RI belum dapat dipastikan",
                    "Cell kandidat nomor kosong atau label tidak cocok dengan posisi pola.",
                    row_number,
                    [number_cell.column],
                    new_candidate,
                )
            if header.supplier.status == "UNRESOLVED":
                add_anomaly(
                    "supplier_unresolved",
                    "Pemasok belum dapat dipastikan",
                    "Cell pemasok kosong atau label pemasok tidak terkonfirmasi.",
                    row_number,
                    [supplier_cell.column],
                    new_candidate,
                )
            continue

        date_label = row_labels.get("Tanggal")
        if date_label is not None:
            if active_candidate is not None:
                date_cell = row_cells[_FIELD_COLUMNS["date"] - 1]
                matched = date_label.column == _HEADER_LABELS["Tanggal"]
                active_candidate.header.date = field_value(
                    date_cell,
                    "date",
                    label_confirmed=matched,
                )
                active_candidate.detection_evidence.extend(
                    [
                        evidence("date_label", "Label tanggal RI", date_label, 3),
                        evidence("date_value", "Cell nilai tanggal berdasarkan label", date_cell, 5),
                    ]
                )
                active_candidate.end_row = row_number
                if not matched or active_candidate.header.date.status == "UNRESOLVED":
                    add_anomaly(
                        "date_unresolved",
                        "Tanggal RI belum dapat dipastikan",
                        "Tanggal kosong atau label tidak berada pada posisi pola.",
                        row_number,
                        [date_label.column, date_cell.column],
                        active_candidate,
                    )
            continue

        detail_header_cells = {
            label: row_labels[label]
            for label in _DETAIL_LABELS
            if label in row_labels
        }
        if len(detail_header_cells) >= 3:
            table_header_active = True
            page_table_header_count += 1
            expected_matches = all(
                label in detail_header_cells
                and detail_header_cells[label].column == expected_column
                for label, expected_column in _DETAIL_LABELS.items()
            )
            for label, label_cell in detail_header_cells.items():
                if active_candidate is not None:
                    active_candidate.detection_evidence.append(
                        evidence(
                            f"detail_label_{_label_key(label)}",
                            f"Label kolom detail: {label}",
                            label_cell,
                            _DETAIL_LABELS[label],
                        )
                    )
            if active_candidate is not None:
                if page_number not in active_candidate.page_numbers:
                    active_candidate.page_numbers.append(page_number)
                active_candidate.end_row = row_number
            if not expected_matches and active_candidate is not None:
                active_candidate.confidence = "MEDIUM"
                add_anomaly(
                    "detail_header_position_mismatch",
                    "Posisi label detail berbeda dari pola",
                    "Label detail terdeteksi, tetapi satu atau lebih label tidak berada pada posisi yang diharapkan.",
                    row_number,
                    [cell.column for cell in detail_header_cells.values()],
                    active_candidate,
                )
            continue

        expected_cells = {
            "item_code": row_cells[_FIELD_COLUMNS["item_code"] - 1],
            "item_name": row_cells[_FIELD_COLUMNS["item_name"] - 1],
            "quantity": row_cells[_FIELD_COLUMNS["quantity"] - 1],
            "unit": row_cells[_FIELD_COLUMNS["unit"] - 1],
        }
        populated_fields = {
            name: cell
            for name, cell in expected_cells.items()
            if cell.value is not None and cell.value != ""
        }
        if not populated_fields:
            if active_candidate is not None:
                active_candidate.end_row = row_number
            continue
        fields = {
            name: field_value(cell, name)
            for name, cell in expected_cells.items()
        }
        if "quantity" in populated_fields and not (
            {"item_code", "item_name", "unit"} & populated_fields.keys()
        ):
            unresolved_rows.append(
                UnresolvedRow(
                    row_number=row_number,
                    page_number=page_number,
                    reason_code="quantity_only",
                    reason="Kuantitas ditemukan tanpa kode, nama, atau satuan; bukan detail yang dipastikan.",
                    fields=fields,
                )
            )
            page_unresolved_count += 1
            add_anomaly(
                "quantity_only",
                "Baris kuantitas saja",
                "Makna baris kuantitas saja belum diketahui; dipertahankan sebagai unresolved.",
                row_number,
                [_FIELD_COLUMNS["quantity"]],
                active_candidate,
            )
            continue

        if not table_header_active:
            reason_code = (
                "detail_without_document_header"
                if active_candidate is None
                else "detail_without_table_header"
            )
            reason = (
                "Baris menyerupai detail tanpa header RI atau header tabel pada halaman ini."
                if active_candidate is None
                else "Baris menyerupai detail, tetapi header tabel tidak terdeteksi."
            )
            unresolved_rows.append(
                UnresolvedRow(
                    row_number=row_number,
                    page_number=page_number,
                    reason_code=reason_code,
                    reason=reason,
                    fields=fields,
                )
            )
            page_unresolved_count += 1
            add_anomaly(
                reason_code,
                "Baris detail tanpa konteks layout lengkap",
                reason,
                row_number,
                [_FIELD_COLUMNS[name] for name in populated_fields],
                active_candidate,
            )
            if fields["unit"].status == "UNRESOLVED":
                add_anomaly(
                    "unit_missing",
                    "Satuan kosong",
                    "Satuan pada baris detail unresolved dibiarkan kosong.",
                    row_number,
                    [_FIELD_COLUMNS["unit"]],
                    active_candidate,
                )
            continue

        if active_candidate is None:
            unresolved_rows.append(
                UnresolvedRow(
                    row_number=row_number,
                    page_number=page_number,
                    reason_code="detail_without_document_header",
                    reason="Baris menyerupai detail, tetapi tidak ada header RI yang dapat ditautkan pada halaman ini.",
                    fields=fields,
                )
            )
            page_unresolved_count += 1
            add_anomaly(
                "detail_without_document_header",
                "Detail tanpa header dokumen",
                "Baris detail tidak diwariskan ke dokumen halaman sebelumnya atau berikutnya.",
                row_number,
                [_FIELD_COLUMNS[name] for name in populated_fields],
            )
            if fields["unit"].status == "UNRESOLVED":
                add_anomaly(
                    "unit_missing",
                    "Satuan kosong",
                    "Satuan pada baris detail unresolved dibiarkan kosong.",
                    row_number,
                    [_FIELD_COLUMNS["unit"]],
                )
            continue

        detail = RIDetailCandidate(
            row_number=row_number,
            item_code=fields["item_code"],
            item_name=fields["item_name"],
            quantity=fields["quantity"],
            unit=fields["unit"],
            status="CANDIDATE",
        )
        active_candidate.details.append(detail)
        active_candidate.end_row = row_number
        active_candidate.detection_evidence.extend(
            evidence(
                f"detail_value_{name}",
                f"Cell kandidat detail {name}",
                cell,
                _FIELD_COLUMNS[name],
            )
            for name, cell in expected_cells.items()
        )
        if page_number not in active_candidate.page_numbers:
            active_candidate.page_numbers.append(page_number)
        page_detail_count += 1
        core_fields = ("item_code", "item_name", "quantity")
        if any(fields[name].status == "UNRESOLVED" for name in core_fields):
            detail.status = "HOLD"
            detail.anomaly_codes.append("partial_detail")
            add_anomaly(
                "partial_detail",
                "Baris detail tidak lengkap",
                "Satu atau lebih field detail kosong; nilai kosong tidak dilengkapi.",
                row_number,
                [
                    _FIELD_COLUMNS[name]
                    for name in core_fields
                    if fields[name].status == "UNRESOLVED"
                ],
                active_candidate,
            )
        if fields["unit"].status == "UNRESOLVED":
            detail.status = "HOLD"
            detail.anomaly_codes.append("unit_missing")
            add_anomaly(
                "unit_missing",
                "Satuan kosong",
                "Satuan dibiarkan kosong dan detail ditahan untuk review.",
                row_number,
                [_FIELD_COLUMNS["unit"]],
                active_candidate,
            )
        for name, value in fields.items():
            if value.raw_value is None and merged_range(row_number, _FIELD_COLUMNS[name]):
                detail.status = "HOLD"
                detail.anomaly_codes.append("merged_blank_not_inherited")
                add_anomaly(
                    "merged_blank_not_inherited",
                    "Cell kosong pada merged range",
                    "Cell anggota merged range tetap kosong; nilai dari cell lain tidak diwariskan.",
                    row_number,
                    [_FIELD_COLUMNS[name]],
                    active_candidate,
                )
        if fields["item_code"].status == "PRESENT":
            duplicate = next(
                (
                    existing
                    for existing in active_candidate.details[:-1]
                    if existing.item_code.normalized_value
                    == fields["item_code"].normalized_value
                ),
                None,
            )
            if duplicate is not None:
                detail.status = "HOLD"
                duplicate.status = "HOLD"
                detail.anomaly_codes.append("repeated_item_code")
                duplicate.anomaly_codes.append("repeated_item_code")
                add_anomaly(
                    "repeated_item_code",
                    "Kode barang berulang pada baris berbeda",
                    "Baris tetap dipisahkan; makna pengulangan belum disetujui.",
                    row_number,
                    [_FIELD_COLUMNS["item_code"]],
                    active_candidate,
                )
                anomalies[-1].source_locators.insert(
                    0, duplicate.item_code.source_locator
                )

    if active_candidate is not None:
        active_candidate.end_row = worksheet.max_row
    if page_has_content:
        close_page(worksheet.max_row)

    _flag_repeated_document_numbers(candidates, anomalies)
    held_pages = {
        anomaly.page_number for anomaly in anomalies if anomaly.page_number is not None
    }
    for page in page_summaries:
        if page.page_number in held_pages:
            page.status = "HOLD"
    for candidate in candidates:
        matched_labels = {
            item.code
            for item in candidate.detection_evidence
            if item.position_matched is True
        }
        required_label_codes = {
            "document_number_label",
            "supplier_label",
            "date_label",
            "detail_label_kode",
            "detail_label_nama_barang",
            "detail_label_kuantitas",
            "detail_label_satuan",
        }
        style_evidence = [
            item
            for item in candidate.detection_evidence
            if item.code in required_label_codes
        ]
        has_style = bool(style_evidence) and all(
            item.style_id is not None for item in style_evidence
        )
        has_merge = any(item.merged_range for item in candidate.detection_evidence)
        if required_label_codes.issubset(matched_labels) and has_style and has_merge:
            candidate.confidence = "HIGH"
        elif len(matched_labels) >= 4:
            candidate.confidence = "MEDIUM"
        else:
            candidate.confidence = "LOW"
        if candidate.header.date.status == "UNRESOLVED":
            candidate.status = "HOLD"
            if "date_unresolved" not in candidate.anomaly_codes:
                candidate.anomaly_codes.append("date_unresolved")
                anomalies.append(
                    RIAnomaly(
                        code="date_unresolved",
                        title="Tanggal RI tidak ditemukan",
                        reason="Tidak ada label Tanggal yang terkonfirmasi dalam konteks header ini.",
                        candidate_index=candidate.candidate_index,
                        page_number=candidate.page_numbers[0] if candidate.page_numbers else None,
                        source_locators=[
                            locator(candidate.header_row, 3),
                        ],
                    )
                )
        if candidate.status == "CANDIDATE_REVIEW" and candidate.details:
            candidate.status = (
                "HOLD"
                if any(detail.status == "HOLD" for detail in candidate.details)
                else "CANDIDATE_REVIEW"
            )
        if candidate.confidence == "HIGH" and not candidate.header.date.source_locator:
            candidate.confidence = "MEDIUM"

    pages_without_header = sum(
        page.document_header_count == 0 and page.unresolved_row_count > 0
        for page in page_summaries
    )
    return RIAnalysisResult(
        source_file_id=source.source_file_id,
        source_filename=source.source_filename,
        source_sha256=source.source_sha256,
        worksheet=WorksheetLayoutMetadata(
            name=worksheet.title,
            sheet_index=sheet_index,
            status=worksheet.sheet_state,
            dimensions=worksheet.calculate_dimension(),
            max_row=worksheet.max_row,
            max_column=worksheet.max_column,
            merged_ranges_count=len(worksheet.merged_cells.ranges),
        ),
        summary=RIAnalysisSummary(
            page_count=len(page_summaries),
            candidate_document_count=len(candidates),
            candidate_detail_count=(
                sum(len(candidate.details) for candidate in candidates)
                + sum(
                    row.reason_code == "detail_without_document_header"
                    for row in unresolved_rows
                )
            ),
            attached_detail_count=sum(len(candidate.details) for candidate in candidates),
            unresolved_row_count=len(unresolved_rows),
            anomaly_count=len(anomalies),
            hold_document_count=sum(candidate.status == "HOLD" for candidate in candidates),
            pages_without_document_header=pages_without_header,
        ),
        anomaly_counts={
            code: sum(anomaly.code == code for anomaly in anomalies)
            for code in sorted({anomaly.code for anomaly in anomalies})
        },
        pages=page_summaries,
        candidates=candidates,
        unresolved_rows=unresolved_rows,
        anomalies=anomalies,
    )


def _normalize_value(field_name: str, value: CellValue) -> CellValue:
    if value is None or value == "":
        return None
    if field_name in {"document_number", "item_code"}:
        return value if isinstance(value, str) else str(value)
    return value


def _row_labels(row_cells: tuple[Cell, ...]) -> dict[str, Cell]:
    expected_labels = set(_HEADER_LABELS) | set(_DETAIL_LABELS)
    labels: dict[str, Cell] = {}
    for cell in row_cells:
        if isinstance(cell.value, str):
            normalized = cell.value.strip().casefold()
            for label in expected_labels:
                if normalized == label.casefold():
                    labels[label] = cell
    return labels


def _page_footer_cell(row_cells: tuple[Cell, ...]) -> Cell | None:
    return next(
        (
            cell
            for cell in row_cells
            if isinstance(cell.value, str) and _PAGE_PATTERN.match(cell.value)
        ),
        None,
    )


def _merged_ranges_by_row(
    worksheet: Worksheet,
) -> dict[int, list[tuple[int, int, str]]]:
    ranges: dict[int, list[tuple[int, int, str]]] = defaultdict(list)
    for merged in worksheet.merged_cells.ranges:
        min_column, min_row, max_column, max_row = merged.bounds
        for row_number in range(min_row, max_row + 1):
            ranges[row_number].append((min_column, max_column, str(merged)))
    return ranges


def _label_key(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.casefold()).strip("_")


def _flag_repeated_document_numbers(
    candidates: list[RIRecordCandidate],
    anomalies: list[RIAnomaly],
) -> None:
    candidates_by_number: dict[str, list[RIRecordCandidate]] = defaultdict(list)
    for candidate in candidates:
        number = candidate.header.document_number.normalized_value
        if isinstance(number, str) and number:
            candidates_by_number[number].append(candidate)
    for number, repeated_candidates in candidates_by_number.items():
        if len(repeated_candidates) < 2:
            continue
        for candidate in repeated_candidates:
            candidate.status = "HOLD"
            if "repeated_document_number" not in candidate.anomaly_codes:
                candidate.anomaly_codes.append("repeated_document_number")
            anomalies.append(
                RIAnomaly(
                    code="repeated_document_number",
                    title="Nomor RI berulang",
                    reason=(
                        f"Nomor RI {number} muncul pada lebih dari satu header. "
                        "Kandidat tidak digabungkan otomatis."
                    ),
                    candidate_index=candidate.candidate_index,
                    page_number=(
                        candidate.page_numbers[0] if candidate.page_numbers else None
                    ),
                    source_locators=[
                        candidate.header.document_number.source_locator
                    ]
                    if candidate.header.document_number.source_locator
                    else [],
                )
            )
