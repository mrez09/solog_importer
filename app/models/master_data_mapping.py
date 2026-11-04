from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.models.mapping import MappingStatus
from app.models.workbook import CellValue, SourceLocator

MasterEntity = Literal["supplier", "item", "unit"]


class MasterSourceWorkbook(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    worksheet_name: str
    worksheet_index: int
    master_observation_count: int


class MasterDataMappingCandidate(BaseModel):
    mapping_id: str
    source_entity: MasterEntity
    source_file_id: str
    source_filename: str
    source_sha256: str
    source_sheet: str
    source_sheet_index: int
    source_field: str
    source_header: str
    source_value: CellValue
    source_data_type: str
    source_locator: SourceLocator
    source_fingerprint: str
    candidate_target_table: str | None
    candidate_target_column: str | None
    target_evidence: Literal["HISTORICAL_SCHEMA_ONLY", "UNKNOWN"]
    target_evidence_note: str
    transformation_proposal: str
    natural_key_proposal: str
    null_handling_proposal: str
    duplicate_handling_proposal: str
    evidence: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    confidence: Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    source_evidence_confidence: Literal["LOW", "MEDIUM", "HIGH"]
    mapping_status: MappingStatus = MappingStatus.REVIEW_REQUIRED
    duplicate_frequency: int = Field(default=1, ge=1)
    duplicate_candidate: bool = False
    conflicting_natural_key: bool = False
    missing_value: bool = False
    candidate_target_id: None = None

    @model_validator(mode="after")
    def candidate_is_not_approved(self) -> "MasterDataMappingCandidate":
        if self.mapping_status not in (
            MappingStatus.DRAFT,
            MappingStatus.REVIEW_REQUIRED,
        ):
            raise ValueError("Kandidat mapping master harus tetap DRAFT atau REVIEW_REQUIRED.")
        if self.candidate_target_id is not None:
            raise ValueError("ID target tidak boleh dibuat dari bukti workbook.")
        if (self.candidate_target_table is None) != (
            self.candidate_target_column is None
        ):
            raise ValueError("Tabel dan kolom kandidat target harus sama-sama diketahui.")
        return self


class MasterDataMappingSummary(BaseModel):
    source_workbook_count: int
    distinct_workbook_sha256_count: int
    candidate_count: int
    supplier_candidate_count: int
    item_candidate_count: int
    unit_candidate_count: int
    missing_value_count: int
    duplicate_candidate_count: int
    conflicting_natural_key_count: int
    mapping_status_counts: dict[str, int]
    target_schema_status: Literal["UNKNOWN"] = "UNKNOWN"


class MasterDataMappingProfile(BaseModel):
    schema_version: int = 1
    source_workbooks: list[MasterSourceWorkbook] = Field(default_factory=list)
    candidates: list[MasterDataMappingCandidate] = Field(default_factory=list)
    summary: MasterDataMappingSummary
    relationship_status: Literal["UNKNOWN"] = "UNKNOWN"
    relationship_note: str


class MasterDataMappingPage(BaseModel):
    profile: MasterDataMappingProfile
    candidates: list[MasterDataMappingCandidate]
    entity_filter: str
    status_filter: str
    page: int
    total_pages: int
    total_filtered: int
