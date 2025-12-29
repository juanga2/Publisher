from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.auth import get_session, require_csrf
from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import Wiki
from app.routers import auth as auth_router
from app.routers import pages as pages_router
from app.routers import render as render_router

app = FastAPI(title="Publisher API")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        existing = db.execute(select(Wiki).where(Wiki.id == "eswiki")).scalar_one_or_none()
        if not existing:
            db.add(
                Wiki(
                    id="eswiki",
                    name="Wikipedia (Español)",
                    api_base="https://es.wikipedia.org/w/api.php",
                    rest_base="https://es.wikipedia.org/api/rest_v1",
                )
            )
            db.commit()


@app.middleware("http")
async def csrf_middleware(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"} and request.url.path.startswith(
        "/api/v1"
    ):
        with SessionLocal() as db:
            session = get_session(request, db)
            if not session:
                return JSONResponse(status_code=401, content={"detail": "not_authenticated"})
            try:
                require_csrf(request, session)
            except Exception:  # noqa: BLE001
                return JSONResponse(status_code=403, content={"detail": "invalid_csrf"})
    return await call_next(request)


@app.get("/")
def root() -> dict:
    return {"status": "ok"}


@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok", "version": settings.version}


app.include_router(auth_router.router)
app.include_router(pages_router.router)
app.include_router(render_router.router)
