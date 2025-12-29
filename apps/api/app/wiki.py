from __future__ import annotations

from typing import Any, Dict

import httpx
from fastapi import HTTPException

from app.models import Wiki


def _build_page_response(wiki: Wiki, page: Dict[str, Any]) -> Dict[str, Any]:
    revisions = page.get("revisions", [])
    latest = revisions[0] if revisions else {}
    content = latest.get("slots", {}).get("main", {}).get("*", "")
    return {
        "wiki_id": wiki.id,
        "page_id": page.get("pageid"),
        "title": page.get("title"),
        "normalized_title": page.get("title"),
        "latest": {
            "rev_id": latest.get("revid"),
            "timestamp": latest.get("timestamp"),
        },
        "content": {"format": "wikitext", "text": content},
        "metadata": {"length_bytes": page.get("length")},
    }


def fetch_page(wiki: Wiki, title: str) -> Dict[str, Any]:
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions|info",
        "rvslots": "main",
        "rvprop": "ids|timestamp|content",
        "redirects": 1,
        "titles": title,
    }
    with httpx.Client(timeout=10) as client:
        response = client.get(wiki.api_base, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="wiki_fetch_failed")
    payload = response.json()
    pages = payload.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)
    if not page or "missing" in page:
        raise HTTPException(status_code=404, detail="page_not_found")
    return _build_page_response(wiki, page)


def render_wikitext(wiki: Wiki, title: str, wikitext: str) -> str:
    rest_url = f"{wiki.rest_base}/transform/wikitext/to/html/{title}"
    rest_payload = {"wikitext": wikitext}
    with httpx.Client(timeout=10) as client:
        rest_response = client.post(rest_url, json=rest_payload)
        if rest_response.status_code == 200:
            return rest_response.text
        parse_params = {
            "action": "parse",
            "format": "json",
            "prop": "text",
            "title": title,
            "contentmodel": "wikitext",
            "text": wikitext,
        }
        parse_response = client.post(wiki.api_base, data=parse_params)
    if parse_response.status_code != 200:
        raise HTTPException(status_code=502, detail="render_failed")
    parsed = parse_response.json()
    html = parsed.get("parse", {}).get("text", {}).get("*")
    if not html:
        raise HTTPException(status_code=502, detail="render_failed")
    return html
