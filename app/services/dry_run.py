from collections import Counter, defaultdict
from math import ceil

from app.models.dry_run import (
    DryRunAuditFinding,
    DryRunCandidate,
    DryRunEntityGroup,
    DryRunMappingPreview,
    DryRunPayloadField,
    DryRunPayloadRecord,
    DryRunPreview,
    DryRunRelationshipPreview,
    DryRunReport,
    DryRunStatus,
    DryRunSummary,
)
from app.models.mapping import (
    MappingDefinition,
    MappingOverride,
    MappingStatus,
    ValidationSeverity,
)
from app.models.ri_candidate import RIAnalysisResult, RIRecordCandidate, UnresolvedRow
from app.services.mapping_engine import build_mapping_definitions, validate_mapping_candidates

DRY_RUN_CANDIDATES_PER_PAGE = 25
DRY_RUN_STATUS_FILTERS = ("ALL", "VALID", "WARNING", "ERROR", "HOLD")


def build_dry_run(
    analysis: RIAnalysisResult,
    overrides: dict[str, MappingOverride] | None = None,
    *,
    page: int = 1,
    status_filter: str = "ALL",
) -> DryRunPreview:
    if status_filter not in DRY_RUN_STATUS_FILTERS:
        raise ValueError("Filter status dry-run tidak dikenal.")

    candidates, _, summary, _, relationships = _evaluate(analysis, overrides)
    selected = [
        candidate
        for candidate in candidates
        if status_filter == "ALL" or candidate.status == status_filter
    ]
    total_pages = max(ceil(len(selected) / DRY_RUN_CANDIDATES_PER_PAGE), 1)
    bounded_page = min(max(page, 1), total_pages)
    start = (bounded_page - 1) * DRY_RUN_CANDIDATES_PER_PAGE
    page_candidates = selected[start : start + DRY_RUN_CANDIDATES_PER_PAGE]
    return DryRunPreview(
        source_file_id=analysis.source_file_id,
        source_filename=analysis.source_filename,
        source_sha256=analysis.source_sha256,
        page=bounded_page,
        total_pages=total_pages,
        status_filter=status_filter,
        summary=summary,
        candidates=page_candidates,
        entity_groups=_build_entity_groups(candidates),
        relationships=relationships,
        report_url=f"/dry-run/{analysis.source_file_id}/report",
    )


def build_dry_run_report(
    analysis: RIAnalysisResult,
    overrides: dict[str, MappingOverride] | None = None,
) -> DryRunReport:
    _, _, summary, findings, relationships = _evaluate(analysis, overrides)
    return DryRunReport(
        source_file_id=analysis.source_file_id,
        source_filename=analysis.source_filename,
        source_sha256=analysis.source_sha256,
        summary=summary,
        findings=findings,
        relationships=relationships,
    )


def _evaluate(
    analysis: RIAnalysisResult,
    overrides: dict[str, MappingOverride] | None,
) -> tuple[
    list[DryRunCandidate],
    list[MappingDefinition],
    DryRunSummary,
    list[DryRunAuditFinding],
    list[DryRunRelationshipPreview],
]:
    definitions = build_mapping_definitions(analysis, overrides or {})
    validations = validate_mapping_candidates(definitions)
    validation_by_id = {item.mapping_id: item for item in validations}
    definitions_by_candidate: dict[str, list[MappingDefinition]] = defaultdict(list)
    for definition in definitions:
        candidate_id = definition.source_candidate_id or f"mapping-{definition.mapping_id}"
        definitions_by_candidate[candidate_id].append(definition)

    source_records: list[
        tuple[
            str,
            str,
            str,
            int,
            list[int],
            str,
            list[str],
            RIRecordCandidate | UnresolvedRow,
        ]
    ] = []
    for candidate in analysis.candidates:
        reasons = _candidate_hold_reasons(candidate)
        source_records.append(
            (
                f"ri-{candidate.candidate_index}",
                "ri_document",
                f"Kandidat RI {candidate.candidate_index}",
                candidate.header_row,
                candidate.page_numbers,
                candidate.status,
                reasons,
                candidate,
            )
        )
    for unresolved in analysis.unresolved_rows:
        source_records.append(
            (
                f"unresolved-{unresolved.row_number}-{unresolved.reason_code}",
                "unresolved_row",
                f"Baris unresolved {unresolved.row_number}",
                unresolved.row_number,
                [unresolved.page_number],
                unresolved.status,
                [unresolved.reason_code, unresolved.reason],
                unresolved,
            )
        )

    candidates: list[DryRunCandidate] = []
    findings: list[DryRunAuditFinding] = []
    for (
        candidate_id,
        candidate_kind,
        label,
        source_row,
        page_numbers,
        source_status,
        source_hold_reasons,
        source_record,
    ) in source_records:
        candidate_definitions = definitions_by_candidate.get(candidate_id, [])
        mapping_previews = [
            DryRunMappingPreview(
                mapping=definition,
                validation=validation_by_id[definition.mapping_id],
                transformation_planned=definition.transformation_rule,
            )
            for definition in candidate_definitions
        ]
        candidate_status = _candidate_status(
            candidate_kind,
            source_status,
            source_hold_reasons,
            mapping_previews,
        )
        mappings_without_target = sum(
            not mapping.mapping.target_entity or not mapping.mapping.target_field
            for mapping in mapping_previews
        )
        mappings_without_approval = sum(
            mapping.mapping.status != MappingStatus.APPROVED
            for mapping in mapping_previews
        )
        candidate = DryRunCandidate(
            candidate_id=candidate_id,
            candidate_kind=candidate_kind,
            label=label,
            source_row=source_row,
            page_numbers=page_numbers,
            source_status=source_status,
            source_hold_reasons=source_hold_reasons,
            status=candidate_status,
            mapping_count=len(mapping_previews),
            mappings_without_target=mappings_without_target,
            mappings_without_approval=mappings_without_approval,
            mappings=mapping_previews,
        )
        candidates.append(candidate)

        for mapping_preview in mapping_previews:
            mapping = mapping_preview.mapping
            for issue in mapping_preview.validation.issues:
                findings.append(
                    DryRunAuditFinding(
                        severity=issue.severity.value,
                        code=issue.code,
                        message=issue.message,
                        candidate_id=candidate_id,
                        mapping_id=mapping.mapping_id,
                        target_candidate=_target_candidate(mapping),
                        source_locator=mapping.source_locator,
                    )
                )
            if mapping.status != MappingStatus.APPROVED:
                findings.append(
                    DryRunAuditFinding(
                        severity=(
                            "ERROR"
                            if mapping.status == MappingStatus.REJECTED
                            else "HOLD"
                        ),
                        code="mapping_not_approved",
                        message=(
                            f"Status mapping {mapping.status} tidak merupakan approval; "
                            "mapping ini tidak diperlakukan sebagai APPROVED."
                        ),
                        candidate_id=candidate_id,
                        mapping_id=mapping.mapping_id,
                        target_candidate=_target_candidate(mapping),
                        source_locator=mapping.source_locator,
                    )
                )

        if source_hold_reasons:
            for reason in source_hold_reasons:
                findings.append(
                    DryRunAuditFinding(
                        severity="HOLD",
                        code="source_candidate_hold",
                        message=reason,
                        candidate_id=candidate_id,
                        source_locator=_first_source_locator(source_record),
                    )
                )

    relationship = DryRunRelationshipPreview(
        relationship="PO–RI",
        reason=(
            "UNKNOWN — tidak ada dasar mapping relasi yang terverifikasi. "
            "Keputusan REL-01 masih NEEDS EVIDENCE; relasi tidak dibuat atau ditebak."
        ),
    )
    relationships = [relationship]
    findings.append(
        DryRunAuditFinding(
            severity="HOLD",
            code="relationship_unknown",
            message=relationship.reason,
        )
    )

    incomplete_candidates = [
        candidate
        for candidate in candidates
        if candidate.mappings_without_target > 0
    ]
    candidates_without_target = sum(
        not any(
            mapping.mapping.target_entity and mapping.mapping.target_field
            for mapping in candidate.mappings
        )
        for candidate in candidates
    )
    issue_severities = Counter(
        issue.severity.value
        for validation in validations
        for issue in validation.issues
    )
    summary = DryRunSummary(
        total_source_candidates=len(candidates),
        total_mappings=len(definitions),
        valid_candidates=sum(candidate.status == "VALID" for candidate in candidates),
        warning_candidates=sum(candidate.status == "WARNING" for candidate in candidates),
        error_candidates=sum(candidate.status == "ERROR" for candidate in candidates),
        hold_candidates=sum(candidate.status == "HOLD" for candidate in candidates),
        candidates_without_target_mapping=candidates_without_target,
        candidates_with_incomplete_target_mapping=len(incomplete_candidates),
        mappings_without_target_mapping=sum(
            candidate.mappings_without_target for candidate in candidates
        ),
        candidates_without_approval=sum(
            candidate.mappings_without_approval > 0 for candidate in candidates
        ),
        mappings_without_approval=sum(
            candidate.mappings_without_approval for candidate in candidates
        ),
        validation_error_count=issue_severities[ValidationSeverity.ERROR.value],
        validation_warning_count=issue_severities[ValidationSeverity.WARNING.value],
    )
    return candidates, definitions, summary, findings, relationships


def _candidate_status(
    candidate_kind: str,
    source_status: str,
    source_hold_reasons: list[str],
    mappings: list[DryRunMappingPreview],
) -> DryRunStatus:
    if candidate_kind == "unresolved_row" or source_status == "HOLD" or source_hold_reasons:
        return "HOLD"
    if any(item.mapping.status == MappingStatus.HOLD for item in mappings):
        return "HOLD"
    if any(item.mapping.status == MappingStatus.REJECTED for item in mappings):
        return "ERROR"
    if not mappings or any(
        item.mapping.status != MappingStatus.APPROVED for item in mappings
    ):
        return "HOLD"
    if any(
        item.validation.evaluation_status == "HOLD"
        or any(
            issue.severity == ValidationSeverity.ERROR
            for issue in item.validation.issues
        )
        for item in mappings
    ):
        return "ERROR"
    if any(item.validation.issues for item in mappings):
        return "WARNING"
    return "VALID"


def _candidate_hold_reasons(candidate: RIRecordCandidate) -> list[str]:
    reasons = list(candidate.anomaly_codes)
    for detail in candidate.details:
        if detail.status == "HOLD":
            reasons.extend(detail.anomaly_codes or ["Detail sumber berstatus HOLD."])
    if candidate.status == "HOLD" and not reasons:
        reasons.append("Kandidat sumber Stage 4.2.3 berstatus HOLD.")
    return list(dict.fromkeys(reasons))


def _first_source_locator(
    source_record: RIRecordCandidate | UnresolvedRow,
):
    if isinstance(source_record, RIRecordCandidate):
        return source_record.header.document_number.source_locator
    if isinstance(source_record, UnresolvedRow):
        return next(
            (
                value.source_locator
                for value in source_record.fields.values()
                if value.source_locator is not None
            ),
            None,
        )
    return None


def _target_candidate(mapping: MappingDefinition) -> str | None:
    if mapping.target_entity and mapping.target_field:
        return f"{mapping.target_entity}.{mapping.target_field}"
    return None


def _build_entity_groups(
    candidates: list[DryRunCandidate],
) -> list[DryRunEntityGroup]:
    grouped: dict[str, list[DryRunPayloadRecord]] = defaultdict(list)
    for candidate in candidates:
        fields_by_entity: dict[str, list[DryRunPayloadField]] = defaultdict(list)
        for preview in candidate.mappings:
            mapping = preview.mapping
            if not mapping.target_entity:
                continue
            fields_by_entity[mapping.target_entity].append(
                DryRunPayloadField(
                    mapping_id=mapping.mapping_id,
                    source_field=mapping.source_field,
                    target_field=mapping.target_field,
                    raw_source_value=mapping.source_value,
                    mapping_status=mapping.status,
                    evaluation_status=preview.validation.evaluation_status,
                    transformation_planned=mapping.transformation_rule,
                    source_locator=mapping.source_locator,
                )
            )
        for entity, fields in fields_by_entity.items():
            grouped[entity].append(
                DryRunPayloadRecord(
                    candidate_id=candidate.candidate_id,
                    candidate_status=candidate.status,
                    fields=fields,
                )
            )
    return [
        DryRunEntityGroup(
            target_entity_placeholder=entity,
            records=records,
        )
        for entity, records in sorted(grouped.items())
    ]
