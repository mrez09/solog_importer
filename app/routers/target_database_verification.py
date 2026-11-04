from datetime import datetime
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import DATA_DIR, settings
from app.models.target_database import (
    TargetDatabaseConfiguration,
    TargetDatabaseProfile,
    TargetEnvironment,
)
from app.security import require_same_origin_and_csrf
from app.services.target_database_storage import (
    TargetDatabaseStorage,
    TargetDatabaseStorageError,
)
from app.services.schema_snapshot import (
    SchemaSnapshotStorage,
    SchemaSnapshotStorageError,
)
from app.services.target_database_verification import (
    SchemaSnapshotCollectionError,
    TargetDatabaseVerificationResult,
    TargetDatabaseVerificationService,
    create_verification_form_token,
    production_confirmation_phrase,
    validate_verification_form_token,
    verification_result_cache,
)

router = APIRouter(prefix="/target-databases", tags=["target-database-verification"])
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")
verification_service = TargetDatabaseVerificationService()


@router.get("/verify", response_class=HTMLResponse, include_in_schema=False)
async def target_database_verification_page(request: Request) -> HTMLResponse:
    return _render_page(request)


@router.post("/{profile_id}/verify", response_class=HTMLResponse, include_in_schema=False)
async def verify_target_database(
    request: Request,
    profile_id: UUID,
    password: str = Form(default=""),
    confirm_target: str = Form(default=""),
    production_confirmation: str = Form(default=""),
    verification_token: str = Form(default=""),
    csrf_token: str = Form(default=""),
    action: str = Form(default="verify"),
) -> HTMLResponse:
    require_same_origin_and_csrf(request, csrf_token)
    configuration = _load_configuration()
    profile = next(
        (item for item in configuration.profiles if item.profile_id == profile_id),
        None,
    )
    if profile is None:
        return _render_page(
            request,
            error="Profil target tidak ditemukan; tidak ada koneksi yang dicoba.",
            configuration=configuration,
            status_code=404,
        )
    if configuration.selected_profile_id != profile.profile_id:
        return _render_page(
            request,
            error="Profil ini bukan target yang sedang dipilih secara eksplisit.",
            configuration=configuration,
            status_code=409,
        )
    if not validate_verification_form_token(verification_token, profile):
        return _render_page(
            request,
            error=(
                "Identitas profil berubah atau formulir kedaluwarsa. Muat ulang "
                "halaman dan tinjau identitas sebelum melanjutkan."
            ),
            configuration=configuration,
            status_code=409,
        )
    if password == "" and profile.environment != TargetEnvironment.LOCAL:
        return _render_page(
            request,
            error=(
                "Password database wajib untuk environment selain Local."
            ),
            configuration=configuration,
            status_code=422,
        )
    if confirm_target != "yes":
        return _render_page(
            request,
            error="Konfirmasi eksplisit atas identitas TARGET wajib dicentang.",
            configuration=configuration,
            status_code=422,
        )
    if (
        profile.environment == TargetEnvironment.PRODUCTION
        and production_confirmation != production_confirmation_phrase(profile)
    ):
        return _render_page(
            request,
            error=(
                "Target Production memerlukan konfirmasi teks yang persis "
                "mengidentifikasi database dan endpoint."
            ),
            configuration=configuration,
            status_code=422,
        )

    if action == "export_schema_snapshot":
        if not _is_requested_snapshot_target(profile):
            return _render_page(
                request,
                error=(
                    "Ekspor snapshot hanya tersedia untuk profil Local "
                    "solog_importer_1 yang telah ditentukan."
                ),
                configuration=configuration,
                status_code=422,
            )
        verification_result_cache.invalidate(profile.profile_id)
        try:
            snapshot = verification_service.collect_schema_snapshot(
                profile,
                password,
                expected_hostname="LAPTOP-H752SMP0",
                expected_engine_version_prefix="10.4.32-MariaDB",
                expected_authenticated_user="devro@localhost",
                expected_effective_user="devro@127.0.0.1",
            )
            captured_at = datetime.fromisoformat(snapshot.captured_at)
            timestamp = captured_at.strftime("%Y%m%d-%H%M%S")
            snapshot_path, digest = SchemaSnapshotStorage().save(
                snapshot,
                timestamp=timestamp,
            )
        except SchemaSnapshotCollectionError as exc:
            return _render_page(
                request,
                error=f"Ekspor snapshot diblokir ({exc.category}): {exc.public_message}",
                configuration=configuration,
                status_code=422,
            )
        except SchemaSnapshotStorageError as exc:
            return _render_page(
                request,
                error=str(exc),
                configuration=configuration,
                status_code=500,
            )
        return _render_page(
            request,
            configuration=configuration,
            snapshot_export={
                "path": snapshot_path.relative_to(DATA_DIR).as_posix(),
                "sha256": digest,
                "collection_status": snapshot.collection_status,
                "summary": snapshot.summary,
                "metadata_gaps": snapshot.metadata_gaps,
            },
        )
    if action != "verify":
        return _render_page(
            request,
            error="Aksi formulir tidak dikenal; tidak ada koneksi yang dicoba.",
            configuration=configuration,
            status_code=422,
        )

    result = verification_service.verify(profile, password)
    verification_result_cache.put(profile, result)
    return _render_page(
        request,
        configuration=configuration,
        result=result,
    )


def _is_requested_snapshot_target(profile: TargetDatabaseProfile) -> bool:
    return (
        profile.environment == TargetEnvironment.LOCAL
        and profile.host == "127.0.0.1"
        and profile.port == 3306
        and profile.database == "solog_importer_1"
        and profile.username == "devro"
    )


def _load_configuration() -> TargetDatabaseConfiguration:
    try:
        return TargetDatabaseStorage().load()
    except TargetDatabaseStorageError as exc:
        raise HTTPException(
            status_code=500,
            detail="Konfigurasi profil target lokal tidak dapat dibaca.",
        ) from exc


def _render_page(
    request: Request,
    *,
    error: str | None = None,
    configuration: TargetDatabaseConfiguration | None = None,
    result: TargetDatabaseVerificationResult | None = None,
    snapshot_export: dict[str, object] | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    configuration = configuration or _load_configuration()
    selected_profile = next(
        (
            profile
            for profile in configuration.profiles
            if profile.profile_id == configuration.selected_profile_id
        ),
        None,
    )
    if result is None and selected_profile is not None:
        result = verification_result_cache.get(selected_profile)
    return templates.TemplateResponse(
        request=request,
        name="target_database_verification.html",
        context={
            "request": request,
            "app_name": settings.app_name,
            "configuration": configuration,
            "selected_profile": selected_profile,
            "verification_token": (
                create_verification_form_token(selected_profile)
                if selected_profile is not None
                else None
            ),
            "production_confirmation_phrase": (
                production_confirmation_phrase(selected_profile)
                if selected_profile is not None
                and selected_profile.environment == TargetEnvironment.PRODUCTION
                else None
            ),
            "password_required": (
                selected_profile is not None
                and selected_profile.environment != TargetEnvironment.LOCAL
            ),
            "error": error,
            "result": result,
            "snapshot_export": snapshot_export,
        },
        status_code=status_code,
    )
