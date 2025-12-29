from __future__ import annotations

from typing import Any, Dict
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from requests_oauthlib import OAuth1Session
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_session, get_session, require_csrf, require_session
from app.config import settings
from app.db import SessionLocal
from app.models import LinkedAccount, User, Wiki
from app.security import encrypt_value, generate_csrf_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _oauth_base(api_base: str) -> str:
    if api_base.endswith("/w/api.php"):
        return api_base[: -len("/w/api.php")]
    return api_base


def _oauth_endpoints(api_base: str) -> Dict[str, str]:
    base = _oauth_base(api_base)
    return {
        "request_token": urljoin(base + "/", "w/index.php?title=Special:OAuth/initiate"),
        "authorize": urljoin(base + "/", "w/index.php?title=Special:OAuth/authorize"),
        "access_token": urljoin(base + "/", "w/index.php?title=Special:OAuth/token"),
        "identify": urljoin(base + "/", "w/index.php?title=Special:OAuth/identify"),
    }


def _oauth_session(token: str | None = None, token_secret: str | None = None) -> OAuth1Session:
    if not settings.oauth_consumer_key or not settings.oauth_consumer_secret:
        raise HTTPException(status_code=500, detail="oauth_not_configured")
    return OAuth1Session(
        client_key=settings.oauth_consumer_key,
        client_secret=settings.oauth_consumer_secret,
        resource_owner_key=token,
        resource_owner_secret=token_secret,
        callback_uri=f"{settings.base_url}/api/v1/auth/eswiki/callback",
    )


def _get_wiki(db: Session, wiki_id: str) -> Wiki:
    wiki = db.get(Wiki, wiki_id)
    if not wiki:
        raise HTTPException(status_code=404, detail="unknown_wiki")
    return wiki


@router.get("/{wiki_id}/start")
def oauth_start(wiki_id: str, response: Response, db: Session = Depends(get_db)) -> Response:
    wiki = _get_wiki(db, wiki_id)
    endpoints = _oauth_endpoints(wiki.api_base)
    oauth = _oauth_session()
    request_token = oauth.fetch_request_token(endpoints["request_token"])

    session = create_session(db, user_id=None)
    session.oauth_request_token = request_token.get("oauth_token")
    session.oauth_request_token_secret = request_token.get("oauth_token_secret")
    db.add(session)
    db.commit()

    auth_url = oauth.authorization_url(endpoints["authorize"])
    response = Response(status_code=307)
    response.headers["Location"] = auth_url
    response.set_cookie(
        settings.session_cookie_name,
        session.id,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/{wiki_id}/callback")
def oauth_callback(
    wiki_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> Response:
    wiki = _get_wiki(db, wiki_id)
    session = get_session(request, db)
    if not session:
        raise HTTPException(status_code=400, detail="missing_session")

    oauth_token = request.query_params.get("oauth_token")
    oauth_verifier = request.query_params.get("oauth_verifier")
    if not oauth_token or not oauth_verifier:
        raise HTTPException(status_code=400, detail="missing_oauth_params")
    if oauth_token != session.oauth_request_token:
        raise HTTPException(status_code=400, detail="oauth_token_mismatch")

    endpoints = _oauth_endpoints(wiki.api_base)
    oauth = _oauth_session(token=session.oauth_request_token, token_secret=session.oauth_request_token_secret)
    access_token = oauth.fetch_access_token(
        endpoints["access_token"],
        verifier=oauth_verifier,
    )

    identify = oauth.get(endpoints["identify"])
    if identify.status_code != 200:
        raise HTTPException(status_code=502, detail="oauth_identify_failed")
    identity = identify.json()
    username = identity.get("username")
    if not username:
        raise HTTPException(status_code=502, detail="oauth_missing_username")

    user = db.execute(select(User).where(User.display_name == username)).scalar_one_or_none()
    if not user:
        user = User(display_name=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    linked = LinkedAccount(
        user_id=user.id,
        wiki_id=wiki.id,
        mw_username=username,
        oauth_token_encrypted=encrypt_value(access_token.get("oauth_token", "")),
        oauth_token_secret_encrypted=encrypt_value(access_token.get("oauth_token_secret", "")),
        scopes=identity.get("grants"),
    )
    db.add(linked)

    session.user_id = user.id
    session.oauth_request_token = None
    session.oauth_request_token_secret = None
    session.csrf_token = generate_csrf_token()
    db.add(session)
    db.commit()

    response = Response(status_code=307)
    response.headers["Location"] = "/"
    response.set_cookie(
        settings.session_cookie_name,
        session.id,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/me")
def auth_me(request: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    session = require_session(request, db)
    user = db.get(User, session.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")

    accounts = db.execute(select(LinkedAccount).where(LinkedAccount.user_id == user.id)).scalars().all()

    # TODO: expose CSRF token to frontend once API contract updated.
    return {
        "user": {"id": user.id, "display_name": user.display_name},
        "linked_accounts": [
            {
                "wiki_id": account.wiki_id,
                "mw_username": account.mw_username,
                "scopes": account.scopes or [],
            }
            for account in accounts
        ],
    }


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> Response:
    session = require_session(request, db)
    require_csrf(request, session)
    db.delete(session)
    db.commit()
    response.delete_cookie(settings.session_cookie_name)
    response.status_code = 204
    return response
