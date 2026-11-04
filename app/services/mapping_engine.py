from collections import Counter
from datetime import date, datetime
from math import ceil

from app.models.mapping import (
    MappingDefinition,
    MappingOverride,
    MappingPreview,
    MappingPreviewRow,
    MappingStatus,
    MappingValidation,
    MappingValidationReport,
    TargetDataType,
    ValidationIssue,
    ValidationSeverity,
)
from app.models.ri_candidate import CandidateValue, RIAnalysisResult

MAPPINGS_PER_PAGE = 25


def build_mapping_preview(
    analysis: RIAnalysisResult,
    overrides: dict[str, MappingOverride],
    page: int = 1,
) -> MappingPreview:
    definitions = build_mapping_definitions(analysis, overrides)
    validations = validate_mapping_candidates(definitions)
    report = _validation_report(definitions, validations)
    total_pages = max(ceil(len(definitions) / MAPPINGS_PER_PAGE), 1)
    bounded_page = min(max(page, 1), total_pages)
    start = (bounded_page - 1) * MAPPINGS_PER_PAGE
    rows = [
        MappingPreviewRow(
            mapping=definition,
            validation=validation,
            target_candidate=(
                f"{definition.target_entity}.{definition.target_field}"
                if definition.target_entity and definition.target_field
                else None
            ),
            transformation_preview=(
                f"{definition.transformation_rule} (belum dijalankan)"
                if definition.transformation_rule
                else "Tidak ada"
            ),
        )
        for definition, validation in zip(
            definitions[start : start + MAPPINGS_PER_PAGE],
            validations[start : start + MAPPINGS_PER_PAGE],
            strict=True,
        )
    ]
    return MappingPreview(
        source_file_id=analysis.source_file_id,
        source_filename=analysis.source_filename,
        source_sha256=analysis.source_sha256,
        page=bounded_page,
        total_pages=total_pages,
        report=report,
        rows=rows,
    )


def build_mapping_definitions(
    analysis: RIAnalysisResult,
    overrides: dict[str, MappingOverride] | None = None,
) -> list[MappingDefinition]:
    overrides = overrides or {}
    definitions: list[MappingDefinition] = []

    def add(
        mapping_id: str,
        source_candidate_id: str,
        candidate_kind: str,
        source_field: str,
        value: CandidateValue,
    ) -> None:
        definition = MappingDefinition(
            mapping_id=mapping_id,
            source_candidate_id=source_candidate_id,
            candidate_kind=candidate_kind,
            source_field=source_field,
            source_value=value.raw_value,
            source_data_type=value.data_type,
            source_status=value.status,
            source_locator=value.source_locator,
        )
        override = overrides.get(mapping_id)
        if override is not None:
            definition = MappingDefinition.model_validate(
                {
                    **definition.model_dump(),
                    **override.model_dump(exclude={"mapping_id"}),
                }
            )
        definitions.append(definition)

    for candidate in analysis.candidates:
        for field_name in ("document_number", "date", "supplier"):
            add(
                f"header-{candidate.candidate_index}-{field_name}",
                f"ri-{candidate.candidate_index}",
                "header",
                f"ri.header.{field_name}",
                getattr(candidate.header, field_name),
            )
        for detail in candidate.details:
            for field_name in ("item_code", "item_name", "quantity", "unit"):
                add(
                    f"detail-{candidate.candidate_index}-{detail.row_number}-{field_name}",
                    f"ri-{candidate.candidate_index}",
                    "detail",
                    f"ri.detail.{field_name}",
                    getattr(detail, field_name),
                )

    for unresolved in analysis.unresolved_rows:
        for field_name, value in unresolved.fields.items():
            add(
                f"unresolved-{unresolved.row_number}-{unresolved.reason_code}-{field_name}",
                f"unresolved-{unresolved.row_number}-{unresolved.reason_code}",
                "unresolved",
                f"ri.detail.{field_name}",
                value,
            )

    return definitions


def validate_mapping(
    mapping: MappingDefinition,
    *,
    duplicate_identity: bool = False,
) -> MappingValidation:
    issues: list[ValidationIssue] = []
    empty = mapping.source_value is None or mapping.source_value == ""

    if not mapping.target_entity or not mapping.target_field:
        issues.append(
            ValidationIssue(
                code="mapping_unresolved",
                severity=ValidationSeverity.ERROR,
                message="Target entity dan target field harus ditinjau sebelum mapping lengkap.",
            )
        )

    if mapping.source_status != "PRESENT" or mapping.source_locator is None:
        issues.append(
            ValidationIssue(
                code="source_unresolved",
                severity=ValidationSeverity.ERROR,
                message="Nilai atau source locator belum terkonfirmasi pada kandidat sumber.",
            )
        )

    if empty:
        required = mapping.target_required is True
        issues.append(
            ValidationIssue(
                code="required_field_empty" if required else "empty_source_value",
                severity=(
                    ValidationSeverity.ERROR
                    if required
                    else ValidationSeverity.WARNING
                ),
                message=(
                    "Field target yang dikonfigurasi wajib memiliki nilai sumber."
                    if required
                    else "Nilai sumber kosong; tidak ada nilai yang diisi otomatis."
                ),
            )
        )

    if mapping.target_data_type is not None and not empty:
        if not _matches_target_type(mapping.source_value, mapping.target_data_type):
            issues.append(
                ValidationIssue(
                    code="data_type_mismatch",
                    severity=ValidationSeverity.ERROR,
                    message=(
                        f"Tipe nilai sumber tidak sesuai dengan tipe target "
                        f"{mapping.target_data_type}."
                    ),
                )
            )

    if mapping.allowed_references and not empty:
        source_reference = str(mapping.source_value)
        if source_reference not in mapping.allowed_references:
            issues.append(
                ValidationIssue(
                    code="invalid_reference",
                    severity=ValidationSeverity.ERROR,
                    message="Nilai sumber tidak ditemukan pada daftar referensi yang dikonfigurasi.",
                )
            )

    if duplicate_identity:
        issues.append(
            ValidationIssue(
                code="duplicate_mapping_candidate",
                severity=ValidationSeverity.ERROR,
                message=(
                    "Source field dan locator yang sama muncul lebih dari sekali; "
                    "baris sumber tidak dihapus atau digabung."
                ),
            )
        )

    if mapping.transformation_rule:
        issues.append(
            ValidationIssue(
                code="transformation_not_executed",
                severity=ValidationSeverity.WARNING,
                message="Aturan transformasi hanya ditampilkan sebagai kandidat dan tidak dijalankan.",
            )
        )

    if mapping.status == MappingStatus.REJECTED:
        evaluation_status = "REJECTED"
    elif mapping.status == MappingStatus.HOLD or any(
        issue.severity == ValidationSeverity.ERROR for issue in issues
    ):
        evaluation_status = "HOLD"
    elif mapping.status != MappingStatus.APPROVED:
        evaluation_status = "REVIEW_REQUIRED"
    else:
        evaluation_status = "VALIDATED"

    return MappingValidation(
        mapping_id=mapping.mapping_id,
        evaluation_status=evaluation_status,
        issues=issues,
    )


def _matches_target_type(value: object, target_type: TargetDataType) -> bool:
    if target_type == TargetDataType.STRING:
        return isinstance(value, str)
    if target_type == TargetDataType.INTEGER:
        return isinstance(value, int) and not isinstance(value, bool)
    if target_type == TargetDataType.NUMBER:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if target_type == TargetDataType.BOOLEAN:
        return isinstance(value, bool)
    if target_type == TargetDataType.DATE:
        return isinstance(value, (date, datetime))
    return False


def _source_identity(mapping: MappingDefinition) -> tuple[str, str, int, str] | None:
    locator = mapping.source_locator
    if locator is None:
        return None
    return (
        mapping.source_field,
        locator.source_file_id,
        locator.sheet_index,
        locator.cell_coordinate or "",
    )


def _validation_report(
    definitions: list[MappingDefinition],
    validations: list[MappingValidation],
) -> MappingValidationReport:
    issues = [issue for validation in validations for issue in validation.issues]
    errors = [
        issue for issue in issues if issue.severity == ValidationSeverity.ERROR
    ]
    warnings = [
        issue for issue in issues if issue.severity == ValidationSeverity.WARNING
    ]
    return MappingValidationReport(
        total_mapped_candidates=len(definitions),
        approved_mappings=sum(item.status == MappingStatus.APPROVED for item in definitions),
        draft_mappings=sum(item.status == MappingStatus.DRAFT for item in definitions),
        review_required=sum(
            item.status == MappingStatus.REVIEW_REQUIRED for item in definitions
        ),
        rejected=sum(item.status == MappingStatus.REJECTED for item in definitions),
        hold=sum(item.status == MappingStatus.HOLD for item in definitions),
        validation_hold_candidates=sum(
            validation.evaluation_status == "HOLD" for validation in validations
        ),
        error_count=len(errors),
        warning_count=len(warnings),
        error_counts=dict(sorted(Counter(issue.code for issue in errors).items())),
        warning_counts=dict(sorted(Counter(issue.code for issue in warnings).items())),
        errors=errors,
        warnings=warnings,
    )


def validate_mapping_candidates(
    definitions: list[MappingDefinition],
) -> list[MappingValidation]:
    identities = Counter(
        identity
        for definition in definitions
        if (identity := _source_identity(definition)) is not None
    )
    return [
        validate_mapping(
            definition,
            duplicate_identity=(
                identity is not None and identities[identity] > 1
                if (identity := _source_identity(definition)) is not None
                else False
            ),
        )
        for definition in definitions
    ]
