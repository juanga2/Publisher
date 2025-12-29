from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Wiki
from app.wiki import fetch_page

router = APIRouter(prefix="/api/v1/pages", tags=["pages"])


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{wiki_id}/{title}")
def get_page(wiki_id: str, title: str, db: Session = Depends(get_db)) -> dict:
    wiki = db.get(Wiki, wiki_id)
    if not wiki:
        raise HTTPException(status_code=404, detail="unknown_wiki")
    return fetch_page(wiki, title)
