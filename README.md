# FusionAI - AI Research Assistant

FusionAI is a full-stack AI research assistant with a FastAPI backend, LangChain-powered retrieval workflow, PostgreSQL-ready persistence, and a React/Vite frontend.

## Features

- AI research answers powered by Anthropic Claude
- Source retrieval from Wikipedia and web search
- PostgreSQL-backed sessions, messages, research results, and citations
- Session document storage for multi-document question answering
- Text, Markdown, and PDF upload support for document-backed QA
- Optional Redis caching for repeated research queries
- FastAPI routes with request logging, timing headers, health, and readiness checks
- Railway-ready backend deployment files

## Tech Stack

**Frontend:** React, Vite, Axios  
**Backend:** Python, FastAPI, SQLAlchemy, LangChain, Anthropic  
**Storage:** PostgreSQL on Railway, SQLite fallback for local development  
**Cache:** Redis when configured, in-memory fallback for development

## Workspace Scope

All session, document, result, research, and chat routes support an optional workspace header:

```http
x-fusion-workspace-id: local-user
```

If the header is missing, the backend uses `DEFAULT_WORKSPACE_ID`, which defaults to `anonymous`. This is lightweight workspace scoping, not full authentication, but it keeps data separated for different users or browser profiles.

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Backend runs on `http://localhost:5001`.

You can verify backend configuration with:

```bash
python scripts/doctor.py
```

For local development, `AUTO_CREATE_TABLES=true` lets the app create SQLite tables automatically.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`.

## Environment Variables

Create `backend/.env` from `backend/.env.example`.

Important values:

```bash
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@host:5432/railway
AUTO_CREATE_TABLES=false
RUN_MIGRATIONS_ON_START=true
DEFAULT_WORKSPACE_ID=anonymous
REDIS_URL=
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=INFO
REQUEST_LOGGING_ENABLED=true
SOURCE_LOOKUP_ENABLED=true
```

If `ANTHROPIC_API_KEY` is missing, the backend still runs and returns local fallback answers. If `DATABASE_URL` is missing, local SQLite is used.

## API Endpoints

```http
GET /api/health
GET /api/ready
POST /api/research
POST /api/chat
POST /api/sessions
GET /api/sessions
GET /api/sessions/{session_id}
GET /api/sessions/{session_id}/results
POST /api/sessions/{session_id}/documents
POST /api/sessions/{session_id}/documents/upload
GET /api/sessions/{session_id}/documents
GET /api/documents/{document_id}
DELETE /api/documents/{document_id}
GET /api/results/{result_id}
DELETE /api/sessions/{session_id}
```

Research request:

```json
{
  "query": "PostgreSQL on Railway",
  "session_id": "optional-existing-session-id"
}
```

Document request:

```json
{
  "title": "Architecture Notes",
  "content": "Paste document text here...",
  "source_type": "document"
}
```

Document upload supports `.txt`, `.md`, and `.pdf` files:

```http
POST /api/sessions/{session_id}/documents/upload
Content-Type: multipart/form-data

file=<notes.txt>
title=Optional display title
```

## Railway Deployment

Recommended Railway setup:

1. Create a Railway project.
2. Add a PostgreSQL service.
3. Deploy the `backend` directory as the backend service.
4. Set environment variables from `backend/.env.example`.
5. Make sure `DATABASE_URL`, `ANTHROPIC_API_KEY`, and `FRONTEND_ORIGINS` are configured.
6. Set `AUTO_CREATE_TABLES=false` and `RUN_MIGRATIONS_ON_START=true` for production.
7. Use the included `Procfile` start command.

Railway should provide `PORT` automatically.

Railway can use `/api/ready` for readiness checks. It returns `503` if the database is unavailable or required production configuration is invalid.

## Database Migrations

Alembic migration files live in `backend/migrations`.

```bash
cd backend
alembic upgrade head
```

In production, `RUN_MIGRATIONS_ON_START=true` runs `alembic upgrade head` during application startup.

For schema changes, create a new migration after updating SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe change"
```

## Project Structure

```text
FusionAI/
  backend/
    app.py
    config.py
    database.py
    models.py
    schemas.py
    services/
    scripts/
    tests/
    migrations/
    requirements.txt
    Procfile
  frontend/
    src/
    package.json
    vite.config.js
```

## Testing

```bash
cd backend
python -m pytest tests
```

The tests use SQLite and disable live source lookup, so they do not require an Anthropic key or network calls.

## Author

Bao Tran - George Mason University
