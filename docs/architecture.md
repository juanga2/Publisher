# Architecture Overview

## Stack
- Frontend: Next.js (React)
- Backend: FastAPI (Python)
- ORM: SQLAlchemy + Alembic
- DB: PostgreSQL
- Cache/Jobs: Redis (optional but enabled)
- Auth: MediaWiki OAuth 1.0a
- Deploy: Docker Compose (VPS)

## Principles
- Human-in-the-loop mandatory
- Backend-only secrets
- Patch/diff based editing
- Conservative defaults, unlockable by reputation
- Multi-wiki and multi-user ready by design

## Key Components
- WikiProvider (per wiki)
- TaskProvider (references, maintenance)
- LLM Orchestrator
- Guardrails Engine
- Reputation Engine
