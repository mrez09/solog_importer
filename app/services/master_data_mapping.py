from collections import Counter, defaultdict
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from app.models.mapping import MappingStatus
from app.models.master_data_mapping import (
    MasterDataMappingCandidate,
    MasterDataMappingPage,
    MasterDataMappingProfile,
    MasterDataMappingSummary,
    MasterSourceWorkbook,
)
from app.models.ri_candidate import RIAnalysisResult
from app.models.workbook import CellValue, SourceLocator, WorkbookRecord
from app.services.workbook_storage import WorkbookStorage

MASTER_MAPPINGS_PER_PAGE = 25
MASTER_ENTITIES = ("ALL", "supplier", "item", "unit")
MASTER_MAPPING_STATUSES = tuple(status.value for status in MappingStatus)
_PR_MARKER = "_PR_"
_GRN_MARKER = "_GRN_"
_PR_COLUMNS = {"item_code": 6, "item_name": 8}
_PROFILE_CACHE_KEY: tuple[tuple[str, str, str], ...] | None = None
_PROFILE_CACHE: MasterDataMappingProfile | None = None


class MasterDataMappingError(Exception):
    """Raised when source evidence cannot be safely read or validated."""


def build_master_data_mapping_profile(
    storage: WorkbookStorage | None = None,
) -> MasterDataMappingProfile:
    global _PROFILE_CACHE_KEY, _PROFILE_CACHE
    workbook_storage = storage or WorkbookStorage()
    records = [
        record
        for record in workbook_storage.list_workbooks()
        if _supported_workbook(record)
    ]
    for record in records:
        _verified_source_path(workbook_storage, record)
    cache_key = tuple(
        (record.source_file_id, record.source_sha256, record.source_filename)
        for record in records
    )
    if cache_key == _PROFILE_CACHE_KEY and _PROFILE_CACHE is not None:
        validate_master_data_mapping_profile(_PROFILE_CACHE, records)
        return _PROFILE_CACHE

    observations: list[dict] = []
    sources: list[MasterSourceWorkbook] = []
    observation_counts: Counter[str] = Counter()
    cached_ri: dict[str, RIAnalysisResult] = {}

    for record in records:
        if _GRN_MARKER in record.source_filename.upper():
            analysis = cached_ri.get(record.source_sha256)
            if analysis is None:
                analysis = workbook_storage.analyze_ri_layout(record)
                cached_ri[record.source_sha256] = analysis
            else:
                _verified_source_path(workbook_storage, record)
            rows = _ri_observations(analysis, record)
            observations.extend(rows)
            sheet_name = analysis.worksheet.name
            sheet_index = analysis.worksheet.sheet_index
        else:
            path = _verified_source_path(workbook_storage, record)
            sheet_name, sheet_index, rows = _pr_observations(path, record)
            observations.extend(rows)
        observation_counts[record.source_file_id] = len(rows)

        sources.append(
            MasterSourceWorkbook(
                source_file_id=record.source_file_id,
                source_filename=record.source_filename,
                source_sha256=record.source_sha256,
                worksheet_name=sheet_name,
                worksheet_index=sheet_index,
                master_observation_count=observation_counts[record.source_file_id],
            )
        )

    candidates = _build_candidates(observations)
    status_counts = Counter(candidate.mapping_status.value for candidate in candidates)
    summary = MasterDataMappingSummary(
        source_workbook_count=len(sources),
        distinct_workbook_sha256_count=len({source.source_sha256 for source in sources}),
        candidate_count=len(candidates),
        supplier_candidate_count=sum(
            candidate.source_entity == "supplier" for candidate in candidates
        ),
        item_candidate_count=sum(
            candidate.source_entity == "item" for candidate in candidates
        ),
        unit_candidate_count=sum(
            candidate.source_entity == "unit" for candidate in candidates
        ),
        missing_value_count=sum(candidate.missing_value for candidate in candidates),
        duplicate_candidate_count=sum(
            candidate.duplicate_candidate for candidate in candidates
        ),
        conflicting_natural_key_count=sum(
            candidate.conflicting_natural_key for candidate in candidates
        ),
        mapping_status_counts=dict(status_counts),
    )
    profile = MasterDataMappingProfile(
        source_workbooks=sources,
        candidates=candidates,
        summary=summary,
        relationship_note=(
            "UNKNOWN — tidak ada crosswalk target atau foreign key target yang "
            "disetujui. Nama, kode, dan kemunculan pada laporan tidak membuktikan relasi."
        ),
    )
    validate_master_data_mapping_profile(profile, records)
    _PROFILE_CACHE_KEY = cache_key
    _PROFILE_CACHE = profile
    return profile


def paginate_master_data_mappings(
    profile: MasterDataMappingProfile,
    *,
    page: int = 1,
    entity_filter: str = "ALL",
    status_filter: str = "ALL",
) -> MasterDataMappingPage:
    if entity_filter not in MASTER_ENTITIES:
        raise ValueError("Filter entitas master tidak dikenal.")
    if status_filter not in ("ALL", *MASTER_MAPPING_STATUSES):
        raise ValueError("Filter status mapping tidak dikenal.")

    filtered = [
        candidate
        for candidate in profile.candidates
        if (entity_filter == "ALL" or candidate.source_entity == entity_filter)
        and (status_filter == "ALL" or candidate.mapping_status.value == status_filter)
    ]
    total_pages = max(ceil(len(filtered) / MASTER_MAPPINGS_PER_PAGE), 1)
    bounded_page = min(max(page, 1), total_pages)
    start = (bounded_page - 1) * MASTER_MAPPINGS_PER_PAGE
    return MasterDataMappingPage(
        profile=profile,
        candidates=filtered[start : start + MASTER_MAPPINGS_PER_PAGE],
        entity_filter=entity_filter,
        status_filter=status_filter,
        page=bounded_page,
        total_pages=total_pages,
        total_filtered=len(filtered),
    )


def validate_master_data_mapping_profile(
    profile: MasterDataMappingProfile,
    current_records: Iterable[WorkbookRecord],
) -> None:
    current = {record.source_file_id: record for record in current_records}
    profile_sources = {source.source_file_id: source for source in profile.source_workbooks}
    if len(profile_sources) != len(profile.source_workbooks):
        raise ValueError("Profil berisi identitas workbook sumber duplikat.")

    for source_id, source in profile_sources.items():
        record = current.get(source_id)
        if record is None:
            raise ValueError("Workbook sumber profil sudah tidak tersedia.")
        if (
            source.source_sha256 != record.source_sha256
            or source.source_filename != record.source_filename
        ):
            raise ValueError("Identitas atau hash workbook sumber profil berubah.")

    for candidate in profile.candidates:
        source = profile_sources.get(candidate.source_file_id)
        if source is None or (
            candidate.source_sha256 != source.source_sha256
            or candidate.source_filename != source.source_filename
            or candidate.source_sheet != source.worksheet_name
            or candidate.source_sheet_index != source.worksheet_index
        ):
            raise ValueError("Kandidat tidak terikat pada snapshot workbook sumber.")
        if candidate.source_locator.source_file_id != source.source_file_id:
            raise ValueError("Source locator tidak cocok dengan workbook kandidat.")
        if candidate.source_locator.source_sha256 != source.source_sha256:
            raise ValueError("Source locator tidak cocok dengan SHA-256 workbook.")
        if candidate.mapping_status not in (
            MappingStatus.DRAFT,
            MappingStatus.REVIEW_REQUIRED,
        ):
            raise ValueError("Profil mapping tidak boleh memuat status approval.")
        if candidate.candidate_target_id is not None:
            raise ValueError("Profil mapping tidak boleh membuat ID target.")


def _supported_workbook(record: WorkbookRecord) -> bool:
    filename = record.source_filename.upper()
    return _PR_MARKER in filename or _GRN_MARKER in filename


def _verified_source_path(storage: WorkbookStorage, record: WorkbookRecord) -> Path:
    try:
        return storage._verified_source_path(record)
    except FileNotFoundError as exc:
        raise MasterDataMappingError(
            "Berkas workbook sumber tidak tersedia; kandidat tidak dibuat."
        ) from exc


def _pr_observations(
    path: Path,
    record: WorkbookRecord,
) -> tuple[str, int, list[dict]]:
    workbook = None
    try:
        workbook = load_workbook(path, data_only=True, read_only=False)
        worksheet = workbook.worksheets[0]
        header_rows = []
        for row_number in range(1, worksheet.max_row + 1):
            code_header = worksheet.cell(row_number, _PR_COLUMNS["item_code"]).value
            name_header = worksheet.cell(row_number, _PR_COLUMNS["item_name"]).value
            if code_header == "Kode #" and name_header == "Nama Barang":
                header_rows.append(row_number)
        if not header_rows:
            raise MasterDataMappingError(
                "Header Kode # dan Nama Barang tidak ditemukan pada laporan PR."
            )

        observations: list[dict] = []
        for index, header_row in enumerate(header_rows):
            next_header = (
                header_rows[index + 1] if index + 1 < len(header_rows) else worksheet.max_row + 1
            )
            for row_number in range(header_row + 1, next_header):
                code_cell = worksheet.cell(row_number, _PR_COLUMNS["item_code"])
                name_cell = worksheet.cell(row_number, _PR_COLUMNS["item_name"])
                if _is_blank(code_cell.value) and _is_blank(name_cell.value):
                    continue
                if _is_pr_header(code_cell.value, name_cell.value):
                    continue
                for field_name, header, cell in (
                    ("item_code", "Kode #", code_cell),
                    ("item_name", "Nama Barang", name_cell),
                ):
                    observations.append(
                        _observation(
                            record=record,
                            entity="item",
                            field_name=field_name,
                            source_header=header,
                            value=cell.value,
                            data_type=cell.data_type,
                            locator=_locator(
                                record,
                                worksheet.title,
                                1,
                                row_number,
                                cell.column,
                            ),
                            source_confidence="HIGH",
                        )
                    )
        return worksheet.title, 1, observations
    finally:
        if workbook is not None:
            workbook.close()


def _ri_observations(
    analysis: RIAnalysisResult,
    record: WorkbookRecord,
) -> list[dict]:
    observations: list[dict] = []
    for candidate in analysis.candidates:
        supplier = candidate.header.supplier
        if supplier.source_locator is not None:
            observations.append(
                _observation(
                    record=record,
                    entity="supplier",
                    field_name="supplier_name",
                    source_header="Pemasok",
                    value=supplier.raw_value,
                    data_type=supplier.data_type,
                    locator=_rebind_locator(supplier.source_locator, record),
                    source_confidence="HIGH"
                    if supplier.status == "PRESENT" and candidate.status != "HOLD"
                    else "LOW",
                    extraction_risks=[
                        *candidate.anomaly_codes,
                        *(
                            ["Kandidat RI asal berstatus HOLD; nilai hanya evidence mentah."]
                            if candidate.status == "HOLD"
                            else []
                        ),
                    ],
                )
            )
        for detail in candidate.details:
            for field_name, header, entity, source_value, column in (
                ("item_code", "Kode #", "item", detail.item_code, 6),
                ("item_name", "Nama Barang", "item", detail.item_name, 8),
                ("unit_name", "Satuan", "unit", detail.unit, 16),
            ):
                locator = source_value.source_locator or _locator(
                    record,
                    analysis.worksheet.name,
                    analysis.worksheet.sheet_index,
                    detail.row_number,
                    column,
                )
                observations.append(
                    _observation(
                        record=record,
                        entity=entity,
                        field_name=field_name,
                        source_header=header,
                        value=source_value.raw_value,
                        data_type=source_value.data_type,
                        locator=_rebind_locator(locator, record),
                        source_confidence="HIGH"
                        if source_value.status == "PRESENT"
                        and detail.status != "HOLD"
                        and candidate.status != "HOLD"
                        else "LOW",
                        extraction_risks=[
                            *detail.anomaly_codes,
                            *(
                                ["Kandidat RI asal berstatus HOLD; nilai hanya evidence mentah."]
                                if candidate.status == "HOLD" or detail.status == "HOLD"
                                else []
                            ),
                        ],
                    )
                )
    for unresolved in analysis.unresolved_rows:
        if unresolved.reason_code != "detail_without_document_header":
            continue
        for field_name, header, entity, source_key, column in (
            ("item_code", "Kode #", "item", "item_code", 6),
            ("item_name", "Nama Barang", "item", "item_name", 8),
            ("unit_name", "Satuan", "unit", "unit", 16),
        ):
            source_value = unresolved.fields[source_key]
            locator = source_value.source_locator or _locator(
                record,
                analysis.worksheet.name,
                analysis.worksheet.sheet_index,
                unresolved.row_number,
                column,
            )
            observations.append(
                _observation(
                    record=record,
                    entity=entity,
                    field_name=field_name,
                    source_header=header,
                    value=source_value.raw_value,
                    data_type=source_value.data_type,
                    locator=_rebind_locator(locator, record),
                    source_confidence="LOW",
                    extraction_risks=[
                        f"Baris {unresolved.reason_code}: {unresolved.reason} "
                        "dan tidak ditautkan ke dokumen RI."
                    ],
                )
            )
    return observations


def _observation(
    *,
    record: WorkbookRecord,
    entity: str,
    field_name: str,
    source_header: str,
    value: CellValue,
    data_type: str,
    locator: SourceLocator,
    source_confidence: str,
    extraction_risks: Iterable[str] = (),
) -> dict:
    value_fingerprint = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )
    fingerprint_payload = (
        f"{record.source_sha256}|{locator.sheet_name}|{locator.row_number}|"
        f"{locator.cell_coordinate}|{field_name}|{value_fingerprint}"
    )
    source_fingerprint = sha256(fingerprint_payload.encode("utf-8")).hexdigest()
    target_table, target_column, target_evidence, target_note = _target_candidate(
        entity, field_name
    )
    natural_key, evidence, risks = _candidate_guidance(entity, field_name)
    risks.extend(extraction_risks)
    return {
        "record": record,
        "entity": entity,
        "field_name": field_name,
        "source_header": source_header,
        "value": value,
        "data_type": data_type,
        "locator": locator,
        "source_confidence": source_confidence,
        "source_fingerprint": source_fingerprint,
        "target_table": target_table,
        "target_column": target_column,
        "target_evidence": target_evidence,
        "target_note": target_note,
        "natural_key": natural_key,
        "evidence": evidence,
        "risks": risks,
    }


def _build_candidates(
    observations: list[dict],
) -> list[MasterDataMappingCandidate]:
    frequencies: Counter[tuple[str, str, str]] = Counter()
    item_names_by_code: dict[str, set[str]] = defaultdict(set)
    for item in observations:
        normalized = _normalize(item["value"])
        if normalized is not None:
            frequencies[(item["record"].source_file_id, item["field_name"], normalized)] += 1
    code_by_row: dict[tuple[str, int], str] = {}
    name_by_row: dict[tuple[str, int], str] = {}
    for item in observations:
        key = (item["record"].source_file_id, item["locator"].row_number)
        normalized = _normalize(item["value"])
        if item["field_name"] == "item_code" and normalized is not None:
            code_by_row[key] = normalized
        elif item["field_name"] == "item_name" and normalized is not None:
            name_by_row[key] = normalized
    for key, code in code_by_row.items():
        name = name_by_row.get(key)
        if name is not None:
            item_names_by_code[code].add(name)

    candidates: list[MasterDataMappingCandidate] = []
    for item in observations:
        record = item["record"]
        locator = item["locator"]
        normalized = _normalize(item["value"])
        frequency = (
            frequencies[(record.source_file_id, item["field_name"], normalized)]
            if normalized is not None
            else 0
        )
        duplicate = frequency > 1
        conflicting_key = (
            item["field_name"] == "item_code"
            and normalized is not None
            and len(item_names_by_code.get(normalized, set())) > 1
        )
        mapping_id = sha256(
            (
                f"{record.source_file_id}|{record.source_sha256}|"
                f"{locator.sheet_name}|{item['field_name']}|{locator.cell_coordinate}"
            ).encode("utf-8")
        ).hexdigest()[:24]
        risks = list(dict.fromkeys(item["risks"]))
        if item["target_evidence"] == "UNKNOWN":
            risks.append("Target tabel/kolom belum diketahui.")
        else:
            risks.append("Kandidat target hanya bersumber dari schema historis, bukan target terverifikasi.")
        if duplicate:
            risks.append(
                "Nilai berulang pada laporan; setiap kemunculan dipertahankan dan tidak digabung."
            )
        if conflicting_key:
            risks.append(
                "Kode barang yang sama dikaitkan dengan nama berbeda pada bukti workbook yang tersedia."
            )
        if _is_blank(item["value"]):
            risks.append("Nilai sumber kosong; tidak ada nilai default yang diterapkan.")

        candidates.append(
            MasterDataMappingCandidate(
                mapping_id=mapping_id,
                source_entity=item["entity"],
                source_file_id=record.source_file_id,
                source_filename=record.source_filename,
                source_sha256=record.source_sha256,
                source_sheet=locator.sheet_name,
                source_sheet_index=locator.sheet_index,
                source_field=item["field_name"],
                source_header=item["source_header"],
                source_value=item["value"],
                source_data_type=item["data_type"],
                source_locator=locator,
                source_fingerprint=item["source_fingerprint"],
                candidate_target_table=item["target_table"],
                candidate_target_column=item["target_column"],
                target_evidence=item["target_evidence"],
                target_evidence_note=item["target_note"],
                transformation_proposal="Tidak diusulkan; nilai raw dipertahankan tanpa transformasi.",
                natural_key_proposal=item["natural_key"],
                null_handling_proposal=(
                    "Pertahankan NULL/kosong sebagai UNKNOWN; jangan isi default."
                ),
                duplicate_handling_proposal=(
                    "Tandai kemunculan untuk review; jangan deduplikasi, gabungkan, atau hapus."
                ),
                evidence=item["evidence"],
                risks=list(dict.fromkeys(risks)),
                confidence="LOW",
                source_evidence_confidence=item["source_confidence"],
                mapping_status=MappingStatus.REVIEW_REQUIRED,
                duplicate_frequency=frequency if frequency else 1,
                duplicate_candidate=duplicate,
                conflicting_natural_key=conflicting_key,
                missing_value=_is_blank(item["value"]),
            )
        )
    return candidates


def _target_candidate(entity: str, field_name: str) -> tuple[str | None, str | None, str, str]:
    candidates = {
        ("supplier", "supplier_name"): (
            "contacts",
            "name",
            "HISTORICAL_SCHEMA_ONLY",
            "Kandidat dari docs-migrate/audit/target-audit.md, tabel contacts; "
            "identitas supplier dan relasi ke receipt belum terverifikasi.",
        ),
        ("item", "item_code"): (
            "items",
            "code",
            "HISTORICAL_SCHEMA_ONLY",
            "Kandidat dari docs-migrate/audit/target-audit.md, tabel items; "
            "schema target otoritatif dan keunikan code belum diketahui.",
        ),
        ("item", "item_name"): (
            "items",
            "name",
            "HISTORICAL_SCHEMA_ONLY",
            "Kandidat dari docs-migrate/audit/target-audit.md, tabel items; "
            "nama hanya atribut, bukan identitas yang disetujui.",
        ),
        ("unit", "unit_name"): (
            "pieces",
            "name",
            "HISTORICAL_SCHEMA_ONLY",
            "Kandidat referensi dari target-audit.md; bertentangan dengan "
            "migration-data-dictionary.md yang menyatakan mapping satuan detail belum diketahui.",
        ),
    }
    return candidates.get(
        (entity, field_name),
        (None, None, "UNKNOWN", "Target table/column UNKNOWN."),
    )


def _candidate_guidance(entity: str, field_name: str) -> tuple[str, list[str], list[str]]:
    evidence = [
        "Nilai dibaca dari workbook sumber yang tersimpan dan diverifikasi terhadap SHA-256.",
        "Source locator menunjuk worksheet dan cell fisik; setiap kemunculan tetap terpisah.",
    ]
    risks = []
    if field_name == "item_code":
        return (
            "Kode # dapat ditinjau sebagai atribut lookup item; keunikan/business key belum terbukti.",
            evidence + ["docs-migrate/audit/target-audit.md: tabel items memiliki kolom code."],
            ["Pengulangan kode dapat berasal dari laporan transaksi; bukan bukti duplikasi master."],
        )
    if field_name == "item_name":
        return (
            "Nama Barang hanya atribut deskriptif; jangan gunakan sebagai natural key.",
            evidence + ["docs-migrate/audit/target-audit.md: tabel items memiliki kolom name."],
            ["Nama yang sama tidak membuktikan identitas item yang sama."],
        )
    if entity == "supplier":
        return (
            "Nama pemasok hanya atribut pencarian; tidak ada kode supplier source yang terverifikasi.",
            evidence + ["docs-migrate/decision/mapping-decision-register.md: MASTER-02 masih NEEDS EVIDENCE."],
            ["Jangan cocokkan atau gabungkan pemasok berdasarkan nama saja."],
        )
    if entity == "unit":
        return (
            "Tidak ada natural key unit yang disetujui; nilai hanya label unit pada laporan.",
            evidence + ["docs-migrate/decision/mapping-decision-register.md: GRN-01 masih NEEDS EVIDENCE."],
            ["Nilai kosong tidak boleh diisi dengan unit default atau unit hasil tebakan."],
        )
    return (
        "Natural key UNKNOWN.",
        evidence,
        risks,
    )


def _is_pr_header(code: CellValue, name: CellValue) -> bool:
    return code == "Kode #" and name == "Nama Barang"


def _normalize(value: CellValue) -> str | None:
    if value is None:
        return None
    text = str(value).strip().casefold()
    return text or None


def _is_blank(value: CellValue) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _locator(
    record: WorkbookRecord,
    sheet_name: str,
    sheet_index: int,
    row_number: int,
    column_number: int,
) -> SourceLocator:
    return SourceLocator(
        source_file_id=record.source_file_id,
        source_filename=record.source_filename,
        source_sha256=record.source_sha256,
        sheet_name=sheet_name,
        sheet_index=sheet_index,
        row_number=row_number,
        cell_coordinate=f"{get_column_letter(column_number)}{row_number}",
    )


def _rebind_locator(locator: SourceLocator, record: WorkbookRecord) -> SourceLocator:
    return locator.model_copy(
        update={
            "source_file_id": record.source_file_id,
            "source_filename": record.source_filename,
            "source_sha256": record.source_sha256,
        }
    )
