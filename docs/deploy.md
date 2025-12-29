# Deployment (Docker Compose)

## Services
- web: Next.js frontend
- api: FastAPI backend (uvicorn/gunicorn)
- db: Postgres
- redis: cache/jobs (enabled)

## Environment Variables

### API
Core:
- DATABASE_URL=postgresql+psycopg://USER:PASS@db:5432/app
- REDIS_URL=redis://redis:6379/0
- APP_ENV=production
- APP_BASE_URL=https://your-domain
- SESSION_SECRET=...
- CSRF_SECRET=...
- TOKEN_ENCRYPTION_KEY=...

OpenAI:
- OPENAI_API_KEY=...
- OPENAI_MODEL=gpt-5
- PROMPT_VERSION=v1

MediaWiki:
- MW_USER_AGENT="JuanWikiTool/0.1 (contact: ...)"
- MW_MAXLAG=5
- MW_ESWIKI_OAUTH_CONSUMER_KEY=...
- MW_ESWIKI_OAUTH_CONSUMER_SECRET=...
- MW_ESWIKI_API_BASE=https://es.wikipedia.org/w/api.php
- MW_ESWIKI_REST_BASE=https://es.wikipedia.org/api/rest_v1

### WEB
- NEXT_PUBLIC_API_BASE_URL=https://your-domain/api/v1

## Operations
- Run Alembic migrations on startup (or init job): `alembic upgrade head`
- Enable Postgres backups (VPS cron)
- Structured logs (JSON) with request_id
