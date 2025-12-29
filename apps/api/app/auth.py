import datetime as dt
from typing import Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Session as SessionModel
from app.security import generate_csrf_token


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _ensure_aware(value: dt.datetime) -> dt.datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=dt.timezone.utc)
    return value


def get_session(request: Request, db: Session) -> Optional[SessionModel]:
    session_id = request.cookies.get(settings.session_cookie_name)
    if not session_id:
        return None
    session = db.get(SessionModel, session_id)
    if not session:
        return None
    if _ensure_aware(session.expires_at) < _now():
        db.delete(session)
        db.commit()
        return None
    return session


def require_session(request: Request, db: Session) -> SessionModel:
    session = get_session(request, db)
    if not session:
        raise HTTPException(status_code=401, detail="not_authenticated")
    return session


def require_csrf(request: Request, session: SessionModel) -> None:
    header_token = request.headers.get("x-csrf-token")
    if not header_token or header_token != session.csrf_token:
        raise HTTPException(status_code=403, detail="invalid_csrf")


def create_session(db: Session, user_id: Optional[str]) -> SessionModel:
    csrf_token = generate_csrf_token()
    expires_at = _now() + dt.timedelta(seconds=settings.session_ttl_seconds)
    session = SessionModel(
        user_id=user_id,
        csrf_token=csrf_token,
        expires_at=expires_at,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session
