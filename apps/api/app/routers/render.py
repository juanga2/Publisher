from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Wiki
from app.wiki import render_wikitext

router = APIRouter(prefix="/api/v1/render", tags=["render"])


class RenderRequest(BaseModel):
    title: str
    wikitext: str


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{wiki_id}")
def render(wiki_id: str, payload: RenderRequest, db: Session = Depends(get_db)) -> dict:
    wiki = db.get(Wiki, wiki_id)
    if not wiki:
        raise HTTPException(status_code=404, detail="unknown_wiki")
    html = render_wikitext(wiki, payload.title, payload.wikitext)
    # TODO: sanitize HTML on the frontend before display.
    return {"html": html}
