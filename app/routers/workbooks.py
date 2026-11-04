from pathlib import Path
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Path as ApiPath,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models.workbook import UploadBatchResult, UploadResult
from app.security import require_same_origin_and_csrf
from app.services.workbook_storage import (
    UploadRejectedError,
    WorkbookStorage,
    WorkbookStorageError,
)
from app.services.xlsx_reader import WorkbookReadError

router = APIRouter(prefix="/workbooks", tags=["workbooks"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")
RI_CANDIDATES_PER_PAGE = 20
UNRESOLVED_PER_PAGE = 20
ANOMALIES_PER_PAGE = 20
T = TypeVar("T")


@dataclass
class PageSlice(Generic[T]):
    items: list[T]
    page: int
    total_pages: int
    total_items: int


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def workbook_list(request: Request) -> HTMLResponse:
    try:
        workbooks = WorkbookStorage().list_workbooks()
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return templates.TemplateResponse(
        request=request,
        name="workbooks.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "max_upload_size_bytes": settings.max_upload_size_bytes,
            "workbooks": workbooks,
            "results": [],
        },
    )


@router.post("/upload", response_class=HTMLResponse, include_in_schema=False)
async def upload_workbooks(
    request: Request,
    files: list[UploadFile] = File(...),
    csrf_token: str = Form(default=""),
) -> HTMLResponse:
    require_same_origin_and_csrf(request, csrf_token)
    storage = WorkbookStorage()
    results: list[UploadResult] = []
    for upload in files:
        filename = upload.filename or ""
        try:
            record = await storage.save_upload(upload)
            results.append(
                UploadResult(
                    status="accepted",
                    source_filename=filename,
                    workbook=record,
                )
            )
        except UploadRejectedError as exc:
            results.append(
                UploadResult(
                    status="rejected",
                    source_filename=filename,
                    error=str(exc),
                )
            )
        except WorkbookStorageError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        finally:
            await upload.close()

    try:
        workbooks = storage.list_workbooks()
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    response_model = UploadBatchResult(results=results, workbooks=workbooks)
    template = (
        "workbook_list.html"
        if request.headers.get("HX-Request", "").casefold() == "true"
        else "workbooks.html"
    )
    context = {
        "request": request,
        "app_name": settings.app_name,
        "workbooks": response_model.workbooks,
        "results": response_model.results,
        "max_upload_size_bytes": settings.max_upload_size_bytes,
    }
    return templates.TemplateResponse(
        request=request,
        name=template,
        context=context,
        status_code=207 if any(result.status == "rejected" for result in results) else 201,
    )


@router.get("/{source_file_id}", response_class=HTMLResponse, include_in_schema=False)
async def workbook_detail(request: Request, source_file_id: UUID) -> HTMLResponse:
    storage = WorkbookStorage()
    source_id = source_file_id.hex
    try:
        record = storage.get_workbook(source_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    try:
        workbook = storage.inspect_record(record)
    except FileNotFoundError as exc:
        message = "Salinan workbook tidak ditemukan."
        record = storage.update_read_error(source_id, message)
        return templates.TemplateResponse(
            request=request,
            name="workbook_detail.html",
            context={
                "request": request,
                "app_name": settings.app_name,
                "source": record,
                "workbook": None,
                "error": message,
            },
            status_code=422,
        )
    except (WorkbookReadError, WorkbookStorageError) as exc:
        record = storage.update_read_error(source_id, str(exc))
        return templates.TemplateResponse(
            request=request,
            name="workbook_detail.html",
            context={
                "request": request,
                "app_name": settings.app_name,
                "source": record,
                "workbook": None,
                "error": str(exc),
            },
            status_code=422,
        )

    return templates.TemplateResponse(
        request=request,
        name="workbook_detail.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "source": record,
            "workbook": workbook,
            "error": None,
        },
    )


@router.get(
    "/{source_file_id}/sheets/{sheet_index}/preview",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def worksheet_preview(
    request: Request,
    source_file_id: UUID,
    sheet_index: int = ApiPath(ge=1),
    start_row: int = Query(default=1, ge=1),
    start_column: int = Query(default=1, ge=1),
) -> HTMLResponse:
    storage = WorkbookStorage()
    source_id = source_file_id.hex
    try:
        record = storage.get_workbook(source_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    try:
        page = storage.read_sheet_page(record, sheet_index, start_row, start_column)
    except FileNotFoundError as exc:
        message = "Salinan workbook tidak ditemukan."
        storage.update_read_error(source_id, message)
        raise HTTPException(status_code=422, detail=message) from exc
    except WorkbookReadError as exc:
        storage.update_read_error(source_id, str(exc))
        return templates.TemplateResponse(
            request=request,
            name="worksheet_preview.html",
            context={
                "request": request,
                "source": record,
                "preview_sheet": None,
                "preview_cells": [],
                "start_row": start_row,
                "start_column": start_column,
                "error": str(exc),
            },
            status_code=422,
        )
    except WorkbookStorageError as exc:
        storage.update_read_error(source_id, str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return templates.TemplateResponse(
        request=request,
        name="worksheet_preview.html",
        context={
            "request": request,
            "source": record,
            "preview_sheet": page,
            "preview_cells": page.cells,
            "start_row": start_row,
            "start_column": start_column,
            "error": None,
        },
    )


@router.get(
    "/{source_file_id}/ri-candidates",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def ri_candidate_preview(
    request: Request,
    source_file_id: UUID,
    sheet_index: int = Query(default=1, ge=1),
    candidate_page: int = Query(default=1, ge=1),
    unresolved_page: int = Query(default=1, ge=1),
    anomaly_page: int = Query(default=1, ge=1),
) -> HTMLResponse:
    storage = WorkbookStorage()
    source_id = source_file_id.hex
    try:
        record = storage.get_workbook(source_id)
        analysis = storage.analyze_ri_layout(record, sheet_index)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook tidak ditemukan.") from exc
    except WorkbookStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except WorkbookReadError as exc:
        return templates.TemplateResponse(
            request=request,
            name="ri_candidates.html",
            context={
                "request": request,
                "source": record,
                "analysis": None,
                "error": str(exc),
            },
            status_code=422,
        )

    return templates.TemplateResponse(
        request=request,
        name="ri_candidates.html",
        context={
            "request": request,
            "source": record,
            "analysis": analysis,
            "error": None,
            "candidate_page": candidate_page,
            "candidate_pages": _page_slice(
                analysis.candidates, candidate_page, RI_CANDIDATES_PER_PAGE
            ),
            "unresolved_page": unresolved_page,
            "unresolved_pages": _page_slice(
                analysis.unresolved_rows, unresolved_page, UNRESOLVED_PER_PAGE
            ),
            "anomaly_page": anomaly_page,
            "anomaly_pages": _page_slice(
                analysis.anomalies, anomaly_page, ANOMALIES_PER_PAGE
            ),
        },
    )


def _page_slice(
    items: Sequence[T],
    page: int,
    page_size: int,
) -> PageSlice[T]:
    total_pages = max((len(items) + page_size - 1) // page_size, 1)
    bounded_page = min(page, total_pages)
    start = (bounded_page - 1) * page_size
    return PageSlice(
        items=list(items[start : start + page_size]),
        page=bounded_page,
        total_pages=total_pages,
        total_items=len(items),
    )
