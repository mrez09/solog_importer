from pathlib import Path
from html import escape

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.logging_config import configure_logging
from app.routers.health import router as health_router
from app.routers.workbooks import router as workbooks_router

BASE_DIR = Path(__file__).resolve().parent
configure_logging()

app = FastAPI(title=settings.app_name, docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(health_router)
app.include_router(workbooks_router)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


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
