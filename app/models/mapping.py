from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.workbook import CellValue, SourceLocator


class MappingStatus(StrEnum):
    DRAFT = "DRAFT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    HOLD = "HOLD"


class TargetDataType(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"


class ValidationSeverity(StrEnum):
    ERROR = "ERROR"
    WARNING = "WARNING"


class MappingDefinition(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    mapping_id: str
    source_candidate_id: str | None = None
    candidate_kind: str
    source_field: str
    source_value: CellValue
    source_data_type: str
    source_status: str
    source_locator: SourceLocator | None
    target_entity: str | None = Field(default=None, max_length=120)
    target_field: str | None = Field(default=None, max_length=120)
    target_data_type: TargetDataType | None = None
    target_required: bool | None = None
    allowed_references: list[str] = Field(default_factory=list)
    transformation_rule: str | None = Field(default=None, max_length=500)
    status: MappingStatus = MappingStatus.REVIEW_REQUIRED
    review_notes: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def normalize_optional_text(self) -> "MappingDefinition":
        for field_name in (
            "target_entity",
            "target_field",
            "transformation_rule",
            "review_notes",
        ):
            value = getattr(self, field_name)
            if value is not None:
                normalized = value.strip()
                setattr(self, field_name, normalized or None)
        self.allowed_references = [
            reference.strip()
            for reference in self.allowed_references
            if reference.strip()
        ]
        return self


class MappingOverride(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    mapping_id: str
    target_entity: str | None = Field(default=None, max_length=120)
    target_field: str | None = Field(default=None, max_length=120)
    target_data_type: TargetDataType | None = None
    target_required: bool | None = None
    allowed_references: list[str] = Field(default_factory=list)
    transformation_rule: str | None = Field(default=None, max_length=500)
    status: MappingStatus = MappingStatus.REVIEW_REQUIRED
    review_notes: str | None = Field(default=None, max_length=2000)


class MappingProfile(BaseModel):
    schema_version: int = 1
    source_file_id: str
    source_sha256: str
    overrides: dict[str, MappingOverride] = Field(default_factory=dict)

    @model_validator(mode="after")
    def override_keys_match(self) -> "MappingProfile":
        if any(key != value.mapping_id for key, value in self.overrides.items()):
            raise ValueError("Kunci override mapping harus cocok dengan mapping_id.")
        return self


class ValidationIssue(BaseModel):
    code: str
    severity: ValidationSeverity
    message: str


class MappingValidation(BaseModel):
    mapping_id: str
    evaluation_status: str
    issues: list[ValidationIssue] = Field(default_factory=list)


class MappingPreviewRow(BaseModel):
    mapping: MappingDefinition
    validation: MappingValidation
    target_candidate: str | None
    transformation_preview: str


class MappingValidationReport(BaseModel):
    total_mapped_candidates: int
    approved_mappings: int
    draft_mappings: int
    review_required: int
    rejected: int
    hold: int
    validation_hold_candidates: int
    error_count: int
    warning_count: int
    error_counts: dict[str, int] = Field(default_factory=dict)
    warning_counts: dict[str, int] = Field(default_factory=dict)
    errors: list[ValidationIssue] = Field(default_factory=list)
    warnings: list[ValidationIssue] = Field(default_factory=list)


class MappingPreview(BaseModel):
    source_file_id: str
    source_filename: str
    source_sha256: str
    page: int
    total_pages: int
    report: MappingValidationReport
    rows: list[MappingPreviewRow]
