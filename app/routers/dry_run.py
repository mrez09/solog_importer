from pathlib import Path
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models.mapping import MappingProfile
from app.models.ri_candidate import RIAnalysisResult
from app.models.workbook import WorkbookRecord
from app.services.dry_run import (
    DRY_RUN_STATUS_FILTERS,
    build_dry_run,
    build_dry_run_report,
)
from app.services.mapping_storage import MappingStorage, MappingStorageError
from app.services.workbook_storage import WorkbookStorage, WorkbookStorageError
from app.services.xlsx_reader import WorkbookReadError

router = APIRouter(prefix="/dry-run", tags=["dry-run"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def dry_run_workbooks(request: Request) -> HTMLResponse:
    try:
        workbooks = WorkbookStorage().list_workbooks()
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return templates.TemplateResponse(
        request=request,
        name="dry_run_workbooks.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "workbooks": workbooks,
        },
    )


@router.get("/{source_file_id}/report", include_in_schema=False)
async def dry_run_report(source_file_id: UUID) -> JSONResponse:
    try:
        record, analysis, profile = _load_inputs(source_file_id.hex)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except (WorkbookStorageError, MappingStorageError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except WorkbookReadError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    report = build_dry_run_report(analysis, profile.overrides)
    return JSONResponse(
        content=jsonable_encoder(report),
        headers={
            "Content-Disposition": (
                f'attachment; filename="dry-run-{record.source_file_id}-report.json"'
            )
        },
    )


@router.get("/{source_file_id}", response_class=HTMLResponse, include_in_schema=False)
async def dry_run_preview(
    request: Request,
    source_file_id: UUID,
    page: int = Query(default=1, ge=1),
    status: Literal["ALL", "VALID", "WARNING", "ERROR", "HOLD"] = Query(
        default="ALL"
    ),
) -> HTMLResponse:
    try:
        record, analysis, profile = _load_inputs(source_file_id.hex)
        preview = build_dry_run(
            analysis,
            profile.overrides,
            page=page,
            status_filter=status,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except (WorkbookStorageError, MappingStorageError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except WorkbookReadError as exc:
        return templates.TemplateResponse(
            request=request,
            name="dry_run_preview.html",
            context={
                "request": request,
                "app_name": settings.app_name,
                "source": None,
                "preview": None,
                "error": str(exc),
                "status_filters": DRY_RUN_STATUS_FILTERS,
            },
            status_code=422,
        )
    return templates.TemplateResponse(
        request=request,
        name="dry_run_preview.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "source": record,
            "preview": preview,
            "error": None,
            "status_filters": DRY_RUN_STATUS_FILTERS,
        },
    )


def _load_inputs(
    source_file_id: str,
) -> tuple[WorkbookRecord, RIAnalysisResult, MappingProfile]:
    storage = WorkbookStorage()
    record = storage.get_workbook(source_file_id)
    analysis = storage.analyze_ri_layout(record)
    profile = MappingStorage().load_profile(
        source_file_id,
        record.source_sha256,
    )
    return record, analysis, profile
