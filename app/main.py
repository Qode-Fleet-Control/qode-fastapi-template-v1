"""Entrypoint: `uvicorn app.main:app --reload`."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.request_log import RequestLogMiddleware
from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open pools, warm caches
    yield
    # shutdown: close them


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

# KEEP THIS: one log line per request (status + duration) is what the workspace Monitoring tab charts.
app.add_middleware(RequestLogMiddleware)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(items.router)
