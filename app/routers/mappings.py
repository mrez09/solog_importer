from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import settings
from app.models.mapping import MappingOverride, MappingStatus, TargetDataType
from app.security import require_same_origin_and_csrf
from app.services.mapping_engine import (
    MAPPINGS_PER_PAGE,
    build_mapping_definitions,
    build_mapping_preview,
)
from app.services.mapping_storage import MappingStorage, MappingStorageError
from app.services.workbook_storage import WorkbookStorage, WorkbookStorageError
from app.services.xlsx_reader import WorkbookReadError

router = APIRouter(prefix="/mappings", tags=["mappings"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def mapping_workbooks(request: Request) -> HTMLResponse:
    try:
        workbooks = WorkbookStorage().list_workbooks()
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return templates.TemplateResponse(
        request=request,
        name="mapping_workbooks.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "workbooks": workbooks,
        },
    )


@router.get("/{source_file_id}", response_class=HTMLResponse, include_in_schema=False)
async def mapping_preview(
    request: Request,
    source_file_id: UUID,
    page: int = Query(default=1, ge=1),
) -> HTMLResponse:
    source_id = source_file_id.hex
    try:
        record = WorkbookStorage().get_workbook(source_id)
        analysis = WorkbookStorage().analyze_ri_layout(record)
        profile = MappingStorage().load_profile(source_id, record.source_sha256)
        preview = build_mapping_preview(analysis, profile.overrides, page)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except (WorkbookStorageError, MappingStorageError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except WorkbookReadError as exc:
        return templates.TemplateResponse(
            request=request,
            name="mapping_preview.html",
            context={
                "request": request,
                "app_name": settings.app_name,
                "source": None,
                "preview": None,
                "error": str(exc),
                "mapping_statuses": list(MappingStatus),
                "target_types": list(TargetDataType),
                "mappings_per_page": MAPPINGS_PER_PAGE,
            },
            status_code=422,
        )
    return templates.TemplateResponse(
        request=request,
        name="mapping_preview.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "source": record,
            "preview": preview,
            "error": None,
            "mapping_statuses": list(MappingStatus),
            "target_types": list(TargetDataType),
            "mappings_per_page": MAPPINGS_PER_PAGE,
        },
    )


@router.post("/{source_file_id}/{mapping_id}", include_in_schema=False)
async def update_mapping(
    request: Request,
    source_file_id: UUID,
    mapping_id: str,
    target_entity: str = Form(default=""),
    target_field: str = Form(default=""),
    target_data_type: str = Form(default=""),
    target_required: str = Form(default="unknown"),
    allowed_references: str = Form(default=""),
    transformation_rule: str = Form(default=""),
    status: MappingStatus = Form(default=MappingStatus.REVIEW_REQUIRED),
    review_notes: str = Form(default=""),
    page: int = Form(default=1),
    csrf_token: str = Form(default=""),
) -> RedirectResponse:
    require_same_origin_and_csrf(request, csrf_token)
    source_id = source_file_id.hex
    try:
        record = WorkbookStorage().get_workbook(source_id)
        analysis = WorkbookStorage().analyze_ri_layout(record)
        storage = MappingStorage()
        profile = storage.load_profile(source_id, record.source_sha256)
        definitions = build_mapping_definitions(analysis, profile.overrides)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except (WorkbookStorageError, MappingStorageError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except WorkbookReadError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not any(definition.mapping_id == mapping_id for definition in definitions):
        raise HTTPException(status_code=404, detail="Kandidat mapping tidak ditemukan.")
    if status == MappingStatus.APPROVED and not review_notes.strip():
        raise HTTPException(
            status_code=422,
            detail="Catatan review wajib diisi untuk status APPROVED.",
        )
    try:
        override = MappingOverride(
            mapping_id=mapping_id,
            target_entity=target_entity,
            target_field=target_field,
            target_data_type=target_data_type or None,
            target_required=_parse_required(target_required),
            allowed_references=[
                value.strip()
                for value in allowed_references.splitlines()
                if value.strip()
            ],
            transformation_rule=transformation_rule,
            status=status,
            review_notes=review_notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail="Konfigurasi mapping tidak valid.") from exc

    profile.overrides[mapping_id] = override
    try:
        storage.save_profile(profile)
    except MappingStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RedirectResponse(
        url=f"/mappings/{source_id}?page={max(page, 1)}",
        status_code=303,
    )


def _parse_required(value: str) -> bool | None:
    if value == "yes":
        return True
    if value == "no":
        return False
    if value == "unknown":
        return None
    raise ValueError("Status required harus yes, no, atau unknown.")
