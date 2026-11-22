
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.auth import WebAuthManager
from api.routes import router
from api.sync_history import SyncHistoryStore
from auth_broker.client import DEFAULT_BROKER_URL


load_dotenv()

app = FastAPI(
    title="DREAMEROL FORK SYNC",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

_WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _is_https_request(request: Request) -> bool:
    forwarded = request.headers.get("x-forwarded-proto", "")
    if forwarded.split(",")[0].strip().lower() == "https":
        return True
    return request.url.scheme == "https"


def _origin_allowed(request: Request, origin: str) -> bool:
    parsed = urlsplit(origin.strip())
    host = request.headers.get("host", "").strip().lower()
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or not host:
        return False
    if parsed.netloc.lower() != host:
        return False
    if parsed.scheme == "https":
        return True
    return not _is_https_request(request)


def _cross_site_write(request: Request) -> bool:
    if request.method not in _WRITE_METHODS:
        return False
    if not request.url.path.startswith("/api/"):
        return False
    origin = request.headers.get("origin")
    if origin is not None:
        return not _origin_allowed(request, origin)
    referer = request.headers.get("referer")
    if referer:
        parsed = urlsplit(referer)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return True
        return not _origin_allowed(request, f"{parsed.scheme}://{parsed.netloc}")
    return False


def _apply_security_headers(response, request: Request) -> None:
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline'; script-src 'self'; "
        "connect-src 'self'; object-src 'none'; base-uri 'self'; "
        "frame-ancestors 'none'",
    )
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    if _is_https_request(request):
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )

app.state.auth_manager = WebAuthManager(
    os.getenv("BROKER_URL", DEFAULT_BROKER_URL)
)
app.state.sync_history = SyncHistoryStore()


@app.middleware("http")
async def add_api_no_store_header(request: Request, call_next):
    if _cross_site_write(request):
        response = JSONResponse(
            status_code=403,
            content={"detail": "Origin not allowed."},
        )
    else:
        response = await call_next(request)
    _apply_security_headers(response, request)
    if request.url.path.startswith("/api/") or request.url.path in {"/", "/dashboard"}:
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
    return response


app.include_router(router)

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "DASHBOARD"

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static",
)

if DASHBOARD_DIR.is_dir():
    app.mount(
        "/dashboard/static",
        StaticFiles(directory=DASHBOARD_DIR),
        name="dashboard-static",
    )


@app.get("/healthz")
def healthz():
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
        },
    )


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/dashboard")
def dashboard():
    dashboard_index = DASHBOARD_DIR / "index.html"
    if dashboard_index.is_file():
        return FileResponse(dashboard_index)
    return FileResponse(WEB_DIR / "index.html")

