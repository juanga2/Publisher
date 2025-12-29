# Publisher

Publicador de mejoras en artículos.

## Setup

### Web (Next.js)

```bash
cd apps/web
npm install
npm run dev
```

### API (FastAPI)

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Compose

```bash
cd infra
docker compose up --build
```
