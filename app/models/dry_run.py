from typing import Literal

from pydantic import BaseModel, Field

from app.models.mapping import MappingDefinition, MappingValidation
from app.models.workbook import CellValue, SourceLocator


DryRunStatus = Literal["VALID", "WARNING", "ERROR", "HOLD"]
DryRunSeverity = Literal["ERROR", "WARNING", "HOLD"]


class DryRunMappingPreview(BaseModel):
    mapping: MappingDefinition
    validation: MappingValidation
    transformation_planned: str | None = None
    transformation_executed: Literal[False] = False


class DryRunCandidate(BaseModel):
    candidate_id: str
    candidate_kind: Literal["ri_document", "unresolved_row"]
    label: str
    source_row: int
    page_numbers: list[int] = Field(default_factory=list)
    source_status: str
    source_hold_reasons: list[str] = Field(default_factory=list)
    status: DryRunStatus
    mapping_count: int
    mappings_without_target: int
    mappings_without_approval: int
    mappings: list[DryRunMappingPreview] = Field(default_factory=list)


class DryRunPayloadField(BaseModel):
    mapping_id: str
    source_field: str
    target_field: str | None
    raw_source_value: CellValue
    mapping_status: str
    evaluation_status: str
    transformation_planned: str | None = None
    transformation_executed: Literal[False] = False
    source_locator: SourceLocator | None = None


class DryRunPayloadRecord(BaseModel):
    candidate_id: str
    candidate_status: DryRunStatus
    fields: list[DryRunPayloadField] = Field(default_factory=list)


class DryRunEntityGroup(BaseModel):
    target_entity_placeholder: str
    records: list[DryRunPayloadRecord] = Field(default_factory=list)


class DryRunSummary(BaseModel):
    total_source_candidates: int
    total_mappings: int
    valid_candidates: int
    warning_candidates: int
    error_candidates: int
    hold_candidates: int
    candidates_without_target_mapping: int
    candidates_with_incomplete_target_mapping: int
    mappings_without_target_mapping: int
    candidates_without_approval: int
    mappings_without_approval: int
    validation_error_count: int
    validation_warning_count: int


class DryRunAuditFinding(BaseModel):
    severity: DryRunSeverity
    code: str
    message: str
    candidate_id: str | None = None
    mapping_id: str | None = None
    target_candidate: str | None = None
    source_locator: SourceLocator | None = None


class DryRunRelationshipPreview(BaseModel):
    relationship: str
    status: Literal["UNKNOWN"] = "UNKNOWN"
    disposition: Literal["HOLD"] = "HOLD"
    reason: str
    source_locator: SourceLocator | None = None


class DryRunReport(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    summary: DryRunSummary
    findings: list[DryRunAuditFinding] = Field(default_factory=list)
    relationships: list[DryRunRelationshipPreview] = Field(default_factory=list)


class DryRunPreview(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    page: int
    total_pages: int
    status_filter: str
    summary: DryRunSummary
    candidates: list[DryRunCandidate] = Field(default_factory=list)
    entity_groups: list[DryRunEntityGroup] = Field(default_factory=list)
    relationships: list[DryRunRelationshipPreview] = Field(default_factory=list)
    report_url: str
