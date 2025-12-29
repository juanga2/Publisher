# API Contract (v1)

Base path: `/api/v1`

Auth:
- Session cookie (HttpOnly) after OAuth.
- CSRF token required for all mutating requests (POST/PATCH/DELETE).
- All endpoints return JSON unless noted.

## Health
### GET `/health`
**200**
```json
{ "status": "ok", "version": "0.1.0" }
```

## Auth
### GET `/auth/{wiki_id}/start`
Redirect to MediaWiki OAuth authorization.

### GET `/auth/{wiki_id}/callback`
Handle OAuth callback; create session; persist linked account.

### GET `/auth/me`
**200**
```json
{
  "user": { "id": "u_123", "display_name": "Juan" },
  "linked_accounts": [
    { "wiki_id": "eswiki", "mw_username": "Juangascona", "scopes": ["read","edit"] }
  ]
}
```

### POST `/auth/logout`
**204** (no body)

## Wikis
### GET `/wikis`
**200**
```json
{
  "items": [
    {
      "id": "eswiki",
      "name": "Wikipedia (Español)",
      "api_base": "https://es.wikipedia.org/w/api.php",
      "rest_base": "https://es.wikipedia.org/api/rest_v1"
    }
  ]
}
```

## Feed
### GET `/feed`
Query:
- `wiki_id` (required)
- `task_type` (required) one of: `references`, `maintenance` (links optional future)
- `limit` (default 20)
- `cursor` (optional)

**200**
```json
{
  "items": [
    {
      "candidate_id": "c_abc",
      "wiki_id": "eswiki",
      "task_type": "references",
      "page": {
        "page_id": 12345,
        "title": "Târgu Neamț",
        "rev_id": 987654,
        "url": "https://es.wikipedia.org/wiki/T%C3%A2rgu_Neam%C8%9B",
        "length_bytes": 18234
      },
      "signals": {
        "templates": ["Sin referencias"],
        "categories": ["Categoría:Artículos sin referencias"],
        "estimated_difficulty": "medium"
      }
    }
  ],
  "next_cursor": "eyJwYWdlX2lkIjoyfQ=="
}
```

### POST `/feed/skip`
**Request**
```json
{ "wiki_id": "eswiki", "task_type": "references", "page_id": 12345 }
```
**204**

## Pages
### GET `/pages/{wiki_id}/{title}`
Query optional: `include=content,metadata,templates,categories`
**200**
```json
{
  "wiki_id": "eswiki",
  "page_id": 12345,
  "title": "Târgu Neamț",
  "normalized_title": "Târgu Neamț",
  "latest": { "rev_id": 987654, "timestamp": "2025-12-29T12:00:00Z" },
  "content": { "format": "wikitext", "text": "== Historia ==\n..." },
  "metadata": { "length_bytes": 18234 }
}
```

## Render
### POST `/render/{wiki_id}`
Renders wikitext to HTML.
**Request**
```json
{ "title": "Târgu Neamț", "wikitext": "== Historia ==\n..." }
```
**200**
```json
{ "html": "<h2>Historia</h2>..." }
```

## Drafts
### POST `/drafts`
**Request**
```json
{
  "wiki_id": "eswiki",
  "page_id": 12345,
  "title": "Târgu Neamț",
  "base_rev_id": 987654,
  "task_type": "references",
  "source": "manual"
}
```
**200**
```json
{ "draft_id": "d_001", "status": "editing" }
```

### PATCH `/drafts/{draft_id}`
**Request**
```json
{ "wikitext": "== Historia ==\n... (editado)" }
```
**200**
```json
{ "draft_id": "d_001", "status": "editing" }
```

### GET `/drafts/{draft_id}`
**200**
```json
{
  "draft_id": "d_001",
  "wiki_id": "eswiki",
  "page_id": 12345,
  "base_rev_id": 987654,
  "task_type": "references",
  "status": "editing",
  "wikitext": "...",
  "latest_validation": { "status": "pending", "issues": [] }
}
```

### POST `/drafts/{draft_id}/diff`
**200**
```json
{
  "unified_diff": "@@ -1,4 +1,7 @@\n...",
  "stats": { "lines_added": 3, "lines_removed": 0 }
}
```

### POST `/drafts/{draft_id}/validate`
**200**
```json
{
  "status": "pass",
  "issues": [],
  "metrics": { "risk_score": 0.22, "diff_lines_added": 3, "diff_lines_removed": 0 }
}
```

## LLM
### POST `/llm/proposals`
**Request**
```json
{
  "draft_id": "d_001",
  "provider": "openai",
  "model": "gpt-5",
  "prompt_version": "v1",
  "constraints_profile": "default"
}
```
**200**
```json
{
  "proposal_id": "p_001",
  "draft_id": "d_001",
  "result": {
    "proposed_wikitext": "== Historia ==\n... (nuevo)",
    "explanation": ["Añadida referencia para la afirmación X"],
    "sources": [{ "url": "https://...", "title": "...", "type": "web" }]
  }
}
```

### POST `/drafts/{draft_id}/apply_proposal`
**Request**
```json
{ "proposal_id": "p_001" }
```
**200**
```json
{ "draft_id": "d_001", "status": "editing" }
```

## Publish
### POST `/publish`
**Request**
```json
{
  "draft_id": "d_001",
  "edit_summary": "Añadidas referencias",
  "minor": true,
  "watchlist": "nochange"
}
```
**200**
```json
{
  "publication_id": "pub_001",
  "status": "success",
  "wiki_id": "eswiki",
  "page_id": 12345,
  "old_rev_id": 987654,
  "new_rev_id": 987700,
  "diff_url": "https://es.wikipedia.org/w/index.php?diff=987700&oldid=987654"
}
```

On edit conflict:
- **409**
```json
{ "error": "conflict", "message": "Base revision is outdated", "current_rev_id": 999999 }
```
