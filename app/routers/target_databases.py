import re
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.config import settings
from app.models.target_database import (
    TargetDatabaseConfiguration,
    TargetDatabaseProfile,
    TargetEnvironment,
    is_protected_reference_identity,
)
from app.security import require_same_origin_and_csrf
from app.services.target_database_storage import (
    TargetDatabaseProfileConflictError,
    TargetDatabaseProfileNotFoundError,
    TargetDatabaseStorage,
    TargetDatabaseStorageError,
)
from app.services.target_database_verification import verification_result_cache

router = APIRouter(prefix="/target-databases", tags=["target-databases"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def target_database_list(request: Request) -> HTMLResponse:
    return _render_page(request)


@router.get("/{profile_id}", response_class=HTMLResponse, include_in_schema=False)
async def target_database_detail(request: Request, profile_id: UUID) -> HTMLResponse:
    configuration = _load_configuration()
    if not any(profile.profile_id == profile_id for profile in configuration.profiles):
        raise HTTPException(status_code=404, detail="Profil target tidak ditemukan.")
    return _render_page(request, profile_id=profile_id, configuration=configuration)


@router.post("/create", include_in_schema=False, response_model=None)
async def create_target_database(
    request: Request,
    name: str = Form(default=""),
    environment: str = Form(default=""),
    host: str = Form(default=""),
    port: str = Form(default=""),
    database: str = Form(default=""),
    username: str = Form(default=""),
    password: str = Form(default=""),
    csrf_token: str = Form(default=""),
) -> RedirectResponse | HTMLResponse:
    require_same_origin_and_csrf(request, csrf_token)
    _ = password
    try:
        profile = _build_profile(
            name=name,
            environment=environment,
            host=host,
            port=port,
            database=database,
            username=username,
        )
        TargetDatabaseStorage().create(profile)
    except TargetDatabaseProfileConflictError as exc:
        return _render_page(request, error=str(exc), status_code=409)
    except TargetDatabaseStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValueError as exc:
        return _render_page(request, error=str(exc), status_code=422)
    return RedirectResponse(url="/target-databases", status_code=303)


@router.post("/{profile_id}/update", include_in_schema=False, response_model=None)
async def update_target_database(
    request: Request,
    profile_id: UUID,
    name: str = Form(default=""),
    environment: str = Form(default=""),
    host: str = Form(default=""),
    port: str = Form(default=""),
    database: str = Form(default=""),
    username: str = Form(default=""),
    password: str = Form(default=""),
    csrf_token: str = Form(default=""),
) -> RedirectResponse | HTMLResponse:
    require_same_origin_and_csrf(request, csrf_token)
    _ = password
    storage = TargetDatabaseStorage()
    try:
        configuration = storage.load()
        if not any(profile.profile_id == profile_id for profile in configuration.profiles):
            raise TargetDatabaseProfileNotFoundError("Profil target tidak ditemukan.")
        profile = _build_profile(
            profile_id=profile_id,
            name=name,
            environment=environment,
            host=host,
            port=port,
            database=database,
            username=username,
        )
        storage.update(profile)
        verification_result_cache.invalidate(profile_id)
    except TargetDatabaseProfileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except TargetDatabaseProfileConflictError as exc:
        return _render_page(
            request,
            error=str(exc),
            profile_id=profile_id,
            status_code=409,
        )
    except TargetDatabaseStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValueError as exc:
        return _render_page(
            request,
            error=str(exc),
            profile_id=profile_id,
            status_code=422,
        )
    return RedirectResponse(
        url=f"/target-databases/{profile_id}",
        status_code=303,
    )


@router.post("/{profile_id}/select", include_in_schema=False)
async def select_target_database(
    request: Request,
    profile_id: UUID,
    csrf_token: str = Form(default=""),
) -> RedirectResponse:
    require_same_origin_and_csrf(request, csrf_token)
    try:
        TargetDatabaseStorage().select(profile_id)
    except TargetDatabaseProfileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except TargetDatabaseStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RedirectResponse(url="/target-databases", status_code=303)


@router.post("/{profile_id}/delete", include_in_schema=False)
async def delete_target_database(
    request: Request,
    profile_id: UUID,
    confirm_delete: str = Form(default=""),
    csrf_token: str = Form(default=""),
) -> RedirectResponse:
    require_same_origin_and_csrf(request, csrf_token)
    if confirm_delete != "yes":
        raise HTTPException(
            status_code=422,
            detail="Konfirmasi penghapusan wajib dicentang.",
        )
    try:
        TargetDatabaseStorage().delete(profile_id)
        verification_result_cache.invalidate(profile_id)
    except TargetDatabaseProfileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except TargetDatabaseStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RedirectResponse(url="/target-databases", status_code=303)


def _build_profile(
    *,
    name: str,
    environment: str,
    host: str,
    port: str,
    database: str,
    username: str,
    profile_id: UUID | None = None,
) -> TargetDatabaseProfile:
    if not name.strip():
        raise ValueError("Nama profil wajib diisi.")
    if not host.strip():
        raise ValueError("Host wajib diisi.")
    if not database.strip():
        raise ValueError("Nama database wajib diisi.")
    if not username.strip():
        raise ValueError("Username wajib diisi.")
    if not re.fullmatch(r"[0-9]{1,5}", port):
        raise ValueError("Port harus berupa bilangan bulat antara 1 dan 65535.")
    port_number = int(port)
    if not 1 <= port_number <= 65535:
        raise ValueError("Port harus berupa bilangan bulat antara 1 dan 65535.")
    try:
        target_environment = TargetEnvironment(environment)
    except ValueError as exc:
        raise ValueError(
            "Environment harus Local, Development, Staging, Production, atau Other."
        ) from exc
    if is_protected_reference_identity(host, port_number, database):
        raise ValueError(
            "Identitas database referensi tidak dapat digunakan sebagai TARGET."
        )
    try:
        profile = TargetDatabaseProfile(
            name=name,
            environment=target_environment,
            host=host,
            port=port_number,
            database=database,
            username=username,
            purpose="TARGET",
        )
        return (
            profile
            if profile_id is None
            else profile.model_copy(update={"profile_id": profile_id})
        )
    except ValidationError as exc:
        raise ValueError(
            "Konfigurasi profil tidak valid. Periksa nama, host, database, dan username."
        ) from exc


def _load_configuration() -> TargetDatabaseConfiguration:
    try:
        return TargetDatabaseStorage().load()
    except TargetDatabaseStorageError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _render_page(
    request: Request,
    *,
    error: str | None = None,
    profile_id: UUID | None = None,
    configuration: TargetDatabaseConfiguration | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    configuration = configuration or _load_configuration()
    profile = next(
        (
            item
            for item in configuration.profiles
            if item.profile_id == profile_id
        ),
        None,
    )
    selected_profile = next(
        (
            item
            for item in configuration.profiles
            if item.profile_id == configuration.selected_profile_id
        ),
        None,
    )
    return templates.TemplateResponse(
        request=request,
        name="target_databases.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "configuration": configuration,
            "profile": profile,
            "selected_profile": selected_profile,
            "environments": list(TargetEnvironment),
            "error": error,
        },
        status_code=status_code,
    )
