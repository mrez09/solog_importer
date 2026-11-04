from typing import Literal

from pydantic import BaseModel, Field

from app.models.workbook import CellValue, SourceLocator


class CandidateValue(BaseModel):
    raw_value: CellValue
    normalized_value: CellValue
    data_type: str
    status: Literal["PRESENT", "UNRESOLVED"]
    source_locator: SourceLocator | None


class DetectionEvidence(BaseModel):
    code: str
    description: str
    locator: SourceLocator | None = None
    observed_value: CellValue = None
    style_id: int | None = None
    merged_range: str | None = None
    expected_column: int | None = None
    position_matched: bool | None = None


class RIHeaderCandidate(BaseModel):
    document_number: CandidateValue
    date: CandidateValue
    supplier: CandidateValue


class RIDetailCandidate(BaseModel):
    row_number: int
    item_code: CandidateValue
    item_name: CandidateValue
    quantity: CandidateValue
    unit: CandidateValue
    status: Literal["CANDIDATE", "HOLD"]
    anomaly_codes: list[str] = Field(default_factory=list)


class RIRecordCandidate(BaseModel):
    candidate_index: int
    header_row: int
    end_row: int
    page_numbers: list[int] = Field(default_factory=list)
    header: RIHeaderCandidate
    details: list[RIDetailCandidate] = Field(default_factory=list)
    detection_evidence: list[DetectionEvidence] = Field(default_factory=list)
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    status: Literal["CANDIDATE_REVIEW", "HOLD"]
    anomaly_codes: list[str] = Field(default_factory=list)


class UnresolvedRow(BaseModel):
    row_number: int
    page_number: int
    reason_code: str
    reason: str
    status: Literal["HOLD"] = "HOLD"
    fields: dict[str, CandidateValue]


class RIAnomaly(BaseModel):
    code: str
    title: str
    reason: str
    status: Literal["HOLD"] = "HOLD"
    page_number: int | None = None
    candidate_index: int | None = None
    source_locators: list[SourceLocator] = Field(default_factory=list)


class WorksheetLayoutMetadata(BaseModel):
    name: str
    sheet_index: int
    status: Literal["visible", "hidden", "veryHidden"]
    dimensions: str
    max_row: int
    max_column: int
    merged_ranges_count: int


class PageLayoutSummary(BaseModel):
    page_number: int
    start_row: int
    end_row: int
    document_header_count: int
    repeated_table_header_count: int
    detail_candidate_count: int
    unresolved_row_count: int
    status: Literal["CANDIDATE", "HOLD"]
    footer_locator: SourceLocator | None = None


class RIAnalysisSummary(BaseModel):
    page_count: int
    candidate_document_count: int
    candidate_detail_count: int
    attached_detail_count: int
    unresolved_row_count: int
    anomaly_count: int
    hold_document_count: int
    pages_without_document_header: int


class RIAnalysisResult(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    worksheet: WorksheetLayoutMetadata
    status: Literal["REVIEW_REQUIRED"] = "REVIEW_REQUIRED"
    summary: RIAnalysisSummary
    anomaly_counts: dict[str, int] = Field(default_factory=dict)
    pages: list[PageLayoutSummary] = Field(default_factory=list)
    candidates: list[RIRecordCandidate] = Field(default_factory=list)
    unresolved_rows: list[UnresolvedRow] = Field(default_factory=list)
    anomalies: list[RIAnomaly] = Field(default_factory=list)
