# Backlog (Source of Truth)

> **IMPORTANT FOR CODEX**
> - Implement tickets in order.
> - Do **NOT** change acceptance criteria.
> - Do **NOT** add features beyond what is specified.
> - If something is unclear, leave TODO comments instead of guessing.
> - Keep commits small and reference ticket IDs in commit messages (e.g., "T2.1: Fetch page").

---

## EPIC 0 — Foundation

### T0.1 Monorepo structure
**Acceptance Criteria**
- apps/web (Next.js)
- apps/api (FastAPI)
- infra/docker-compose.yml
- docs/adr/
- README with setup instructions

### T0.2 CI pipeline
**AC**
- Lint + tests + build on PR
- Fail if secrets committed (basic secret scanning)

### T0.3 Docker Compose
**AC**
- Services: web, api, db, redis
- `docker compose up` boots all
- `/api/v1/health` returns 200

---

## EPIC 1 — Authentication & Security

### T1.1 MediaWiki OAuth (ADR-001)
**AC**
- OAuth 1.0a flow works for eswiki
- Tokens stored encrypted in DB
- `/api/v1/auth/me` returns linked account

### T1.2 Session & CSRF (ADR-002)
**AC**
- HttpOnly session cookie
- CSRF required on all mutations
- Logout invalidates session

### T1.3 Token encryption
**AC**
- `oauth_token` and `oauth_token_secret` stored encrypted (Fernet or AES-GCM)
- Master key from env `TOKEN_ENCRYPTION_KEY`

---

## EPIC 2 — MediaWiki Integration

### T2.1 Fetch page
**AC**
- Fetch wikitext + rev_id + basic metadata
- Handle redirects and 404

### T2.2 Render HTML (ADR-003)
**AC**
- Primary: MediaWiki REST HTML
- Fallback: action=parse
- Automatic fallback on failure
- HTML sanitized before display

### T2.3 Publish edit
**AC**
- Edit token usage
- Detect edit conflicts (base_rev mismatch)
- Respect maxlag and rate limiting
- Store publication record

---

## EPIC 3 — Suggested Edits Feed

### T3.1 References TaskProvider (Hybrid)
**AC**
- Discover via categories (maintenance categories for references)
- Verify via wikitext template detection
- Exclude non-main namespaces by default

### T3.2 Maintenance TaskProvider (Hybrid)
**AC**
- Same strategy as references
- Separate `task_type=maintenance`

### T3.3 Skip list
**AC**
- User can skip article candidates
- Skipped items never reappear for that user+wiki+task_type

---

## EPIC 4 — Drafts, Editor & Diff

### T4.1 Draft lifecycle
**AC**
- Create, update, fetch drafts
- Track `base_rev_id`

### T4.2 Diff generation
**AC**
- Server-side unified diff
- Stable output given same inputs
- Line stats computed

### T4.3 Editor UI
**AC**
- 3 panels: editor, diff, render
- Render auto-updates (debounced)
- Publish disabled until validation passes and edit summary present

---

## EPIC 5 — Guardrails & Reputation

### T5.1 Reputation MVP (ADR-004)
**AC**
- Reputation = published_count
- Levels: 0 / 10 / 25 / 50 / 100
- Increment on successful publish
- UI shows level and published_count

### T5.2 Guardrails Pack 1 (ADR-006)
**Default ON**
- Block BLP (conservative heuristic; false positives OK)
- Block sensitive/current topics (conservative heuristic)
- Max diff 20 lines (except refs)
- References task: add-only changes (no rewrites)

**AC**
- Guardrails enforced at validate and at publish
- Toggles visible but locked until reputation allows deselection
- Guardrails policy is configurable via DB (policy JSON)

---

## EPIC 6 — LLM Integration (OpenAI)

### T6.1 LLM Orchestrator
**AC**
- Provider: OpenAI
- Output: full wikitext proposal (backend computes diff)
- Store proposal with `prompt_version`

### T6.2 Prompts ES v1
**AC**
- Spanish prompts
- Separate refs / maintenance
- Hard rules: no hallucinations, NPOV, citations mandatory
- Stored under `/apps/api/prompts/`

### T6.3 Apply proposal
**AC**
- Replace draft wikitext with proposed wikitext
- Auto-generate diff and trigger validation

---

## EPIC 7 — Validation & Observability

### T7.1 Validation engine
**AC**
- Block publication on any blocker
- No manual override in MVP

### T7.2 Audit trail
**AC**
- Drafts, proposals, validations, publications visible
- Publication records include a Wikipedia diff link

---

## EPIC 8 — Future (roadmap only)
- Multi-user (roles, invitations)
- Multi-wiki enablement
- Multi-LLM comparison
- Revert-aware reputation (penalize on reverts)
- Content expansion (add-only sections with sources)
- Article creation (draft → publish)
