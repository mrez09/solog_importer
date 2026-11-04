from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.master_data_mapping import (
    MASTER_ENTITIES,
    MASTER_MAPPING_STATUSES,
    MasterDataMappingError,
    build_master_data_mapping_profile,
    paginate_master_data_mappings,
)
from app.services.workbook_storage import WorkbookStorage, WorkbookStorageError
from app.services.xlsx_reader import WorkbookReadError

router = APIRouter(prefix="/master-data-mappings", tags=["master-data-mappings"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def master_data_mapping_preview(
    request: Request,
    page: int = Query(default=1, ge=1),
    entity: str = Query(default="ALL"),
    status: str = Query(default="ALL"),
) -> HTMLResponse:
    try:
        profile = build_master_data_mapping_profile(WorkbookStorage())
        preview = paginate_master_data_mappings(
            profile,
            page=page,
            entity_filter=entity,
            status_filter=status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except MasterDataMappingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (WorkbookStorageError, WorkbookReadError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return templates.TemplateResponse(
        request=request,
        name="master_data_mappings.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "preview": preview,
            "entities": MASTER_ENTITIES,
            "statuses": MASTER_MAPPING_STATUSES,
        },
    )
