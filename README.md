# FusionAI — AI Research Assistant

FusionAI is a full-stack AI research assistant that combines Wikipedia, web search, and Claude AI to synthesize multi-source answers in seconds. It features a fully animated React frontend, a FastAPI backend with LangChain, and PostgreSQL-backed session persistence.

**Live:** [fusionai.studio](https://www.fusionai.studio)

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18, Vite 5, Tailwind CSS v4, Framer Motion |
| Backend | Python 3.12, FastAPI, LangChain, Anthropic Claude |
| AI | Claude claude-sonnet-4-6 via LangChain direct chain |
| Database | PostgreSQL (Railway), SQLite fallback for local dev |
| ORM | SQLAlchemy 2.x + Alembic migrations |
| DB Driver | psycopg2-binary |
| Cache | Redis (optional), in-memory fallback |
| Backend Host | Railway |
| Frontend Host | Vercel |

---

## Features

- AI research answers powered by Anthropic Claude (claude-sonnet-4-6)
- Smart query intent detection — conversational messages skip web search entirely
- Parallel Wikipedia + DuckDuckGo source fetching for faster responses
- Direct LangChain `prompt | llm` chain (no multi-round agent overhead)
- PostgreSQL-backed sessions, messages, research results, and citations
- Document upload (`.txt`, `.md`, `.pdf`) for document-backed Q&A
- Optional Redis caching for repeated queries
- Fully animated landing page and chat interface (Framer Motion)
- FastAPI with request logging, timing headers, health and readiness endpoints

---

## Local Development

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
copy .env.example .env       # then fill in your values
python app.py
```

Backend runs on `http://localhost:5001`.

Run the config doctor to verify your setup:

```bash
python scripts/doctor.py
```

For local dev, leave `DATABASE_URL` unset to use SQLite with `AUTO_CREATE_TABLES=true`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`. The Vite dev server proxies `/api/*` to `localhost:5001` automatically — no `VITE_API_URL` needed locally.

---

## Environment Variables

### Backend (`backend/.env`)

Copy from `backend/.env.example` and fill in:

```env
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@host:5432/dbname
ENVIRONMENT=production
FRONTEND_ORIGINS=https://www.fusionai.studio,https://your-app.vercel.app
ANTHROPIC_MODEL=claude-sonnet-4-6
MAX_TOKENS=2000
AUTO_CREATE_TABLES=false
RUN_MIGRATIONS_ON_START=false
SOURCE_LOOKUP_ENABLED=true
WIKIPEDIA_RESULTS=1
WEB_SEARCH_RESULTS=3
LOCAL_CACHE_ENABLED=true
CACHE_TTL_SECONDS=1800
LOG_LEVEL=INFO
```

> In production, migrations run via the Procfile (`alembic upgrade head && uvicorn ...`) before the app starts. Keep `RUN_MIGRATIONS_ON_START=false`.

### Frontend (`frontend/.env`)

```env
VITE_API_URL=https://your-railway-backend.up.railway.app
VITE_WORKSPACE_ID=web-client
```

---

## Database Migrations

Alembic migrations live in `backend/migrations/`.

Run manually:

```bash
cd backend
alembic upgrade head
```

In production (Railway), the `Procfile` runs migrations automatically before uvicorn starts:

```
web: alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port $PORT
```

To create a new migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

---

## Deployment

### Railway (Backend)

1. Create a Railway project and add a **PostgreSQL** service
2. Add the backend as a service with **Root Directory** set to `backend`
3. Railway auto-detects Python via `runtime.txt` and uses the `Procfile`
4. Set environment variables in Railway → Variables tab (see above)
5. `DATABASE_URL` should reference your PostgreSQL service: `${{Postgres.DATABASE_URL}}`

Railway exposes `/api/ready` for readiness checks — returns `503` if the database is down or config is invalid.

### Vercel (Frontend)

1. Import the repository in Vercel
2. Set **Root Directory** to `frontend` and framework to **Vite**
3. Add environment variables: `VITE_API_URL` and `VITE_WORKSPACE_ID`
4. Deploy — `VITE_*` vars are baked into the build bundle at deploy time

---

## API Endpoints

```
GET  /api/health
GET  /api/ready
POST /api/research
POST /api/chat
POST /api/sessions
GET  /api/sessions
GET  /api/sessions/{session_id}
GET  /api/sessions/{session_id}/results
POST /api/sessions/{session_id}/documents
POST /api/sessions/{session_id}/documents/upload
GET  /api/sessions/{session_id}/documents
GET  /api/documents/{document_id}
DELETE /api/documents/{document_id}
GET  /api/results/{result_id}
DELETE /api/sessions/{session_id}
GET  /api/insights
```

**Research request:**
```json
{ "query": "what is quantum computing", "session_id": "optional-id" }
```

**Document upload:** `multipart/form-data` with `file` + optional `title` fields.

All routes accept an optional workspace header for data isolation:
```
x-fusion-workspace-id: your-workspace-id
```

---

## Project Structure

```
FusionAI/
├── backend/
│   ├── app.py                  # FastAPI app + lifespan
│   ├── config.py               # Settings + diagnostics
│   ├── database.py             # SQLAlchemy engine + session
│   ├── models.py               # ORM models
│   ├── schemas.py              # Pydantic request/response models
│   ├── services/
│   │   ├── ai.py               # LangChain chain + Claude integration
│   │   ├── sources.py          # Wikipedia + web search + intent detection
│   │   ├── research.py         # Research query orchestration
│   │   ├── sessions.py         # Session management
│   │   ├── cache.py            # Redis + in-memory cache
│   │   ├── documents.py        # Document storage
│   │   ├── uploads.py          # File upload parsing
│   │   ├── insights.py         # Usage analytics
│   │   └── operations.py       # Alembic migration runner
│   ├── migrations/             # Alembic migration files
│   ├── scripts/
│   │   └── doctor.py           # Config health checker
│   ├── tests/                  # pytest test suite
│   ├── requirements.txt
│   ├── Procfile                # Railway start command
│   ├── runtime.txt             # Python version
│   └── alembic.ini
└── frontend/
    ├── src/
    │   ├── App.jsx             # Full app — landing page + research UI
    │   ├── App.css
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

---

## Testing

```bash
cd backend
python -m pytest tests
```

Tests use SQLite and disable live source lookup — no Anthropic key or network required.

---

## Author

Bao Tran — George Mason University
