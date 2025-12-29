import datetime as dt

from fastapi.testclient import TestClient

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.main import app
from app.models import Session as SessionModel


def setup_module() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _create_session(session_id: str) -> tuple[str, str]:
    csrf_token = f"csrf-{session_id}"
    expires_at = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)
    session = SessionModel(
        id=session_id,
        csrf_token=csrf_token,
        expires_at=expires_at,
    )
    with SessionLocal() as db:
        db.add(session)
        db.commit()
    return session_id, csrf_token


def test_logout_requires_csrf() -> None:
    session_id, _csrf_token = _create_session("s_test_1")
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/logout",
        cookies={settings.session_cookie_name: session_id},
    )

    assert response.status_code == 403


def test_logout_with_csrf() -> None:
    session_id, csrf_token = _create_session("s_test_2")
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/logout",
        cookies={settings.session_cookie_name: session_id},
        headers={"x-csrf-token": csrf_token},
    )

    assert response.status_code == 204
