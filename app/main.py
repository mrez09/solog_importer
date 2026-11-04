from pathlib import Path
from html import escape

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from app.config import settings
from app.logging_config import configure_logging
from app.security import CSRF_COOKIE_NAME, issue_csrf_token
from app.routers.health import router as health_router
from app.routers.dry_run import router as dry_run_router
from app.routers.master_data_mappings import router as master_data_mappings_router
from app.routers.mappings import router as mappings_router
from app.routers.target_databases import router as target_databases_router
from app.routers.target_database_verification import (
    router as target_database_verification_router,
)
from app.routers.workbooks import router as workbooks_router

BASE_DIR = Path(__file__).resolve().parent
configure_logging()

app = FastAPI(title=settings.app_name, docs_url=None, redoc_url=None)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "[::1]"],
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(health_router)
app.include_router(workbooks_router)
app.include_router(mappings_router)
app.include_router(master_data_mappings_router)
app.include_router(dry_run_router)
app.include_router(target_database_verification_router)
app.include_router(target_databases_router)
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.middleware("http")
async def apply_security_headers(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    csrf_token = issue_csrf_token(request)
    request.state.csrf_token = csrf_token
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Cache-Control", "no-store")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self' https://unpkg.com; "
        "style-src 'self'; img-src 'self' data:; form-action 'self'; "
        "frame-ancestors 'none'; base-uri 'self'; object-src 'none'",
    )
    if request.url.scheme == "https":
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )
    response.set_cookie(
        CSRF_COOKIE_NAME,
        csrf_token,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="strict",
        path="/",
    )
    return response


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request, "app_name": settings.app_name},
    )


@app.get("/health/status", response_class=HTMLResponse, include_in_schema=False)
async def health_status_fragment() -> HTMLResponse:
    environment = escape(settings.environment)
    return HTMLResponse(
        '<div id="app-status" class="status-pill">'
        '<span class="status-dot"></span> Aplikasi aktif '
        f'<span class="status-environment">{environment}</span></div>'
    )
