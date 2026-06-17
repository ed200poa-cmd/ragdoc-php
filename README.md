# RAGDoc — AI Document Q&A

RAG-powered document Q&A system. Upload a PDF or TXT, ask questions in natural language, get streaming answers with source citations.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | PHP 8.1 (vanilla), HTML/CSS/JS, Server-Sent Events |
| Backend | Python 3.12, FastAPI, Uvicorn |
| AI | Claude claude-sonnet-4-6 (LangChain), OpenAI text-embedding-3-small |
| Vector DB | PostgreSQL 16 + pgvector |
| ORM | SQLAlchemy async + asyncpg |
| Deploy | Railway (Docker) |

## Local Development

```bash
# Copy env vars
cp .env.example .env
# Edit .env with your API keys

# Start everything
docker compose up --build
```

Frontend: http://localhost:8080  
Backend API: http://localhost:8000/docs

## Railway Deployment

### 1. Backend Service
```bash
cd backend
railway login
railway init --name ragdoc-php
railway service create --name ragdoc-backend
railway up --service ragdoc-backend
```

Add PostgreSQL plugin in Railway dashboard, then:
```bash
railway variable set ANTHROPIC_API_KEY=<your-key> --service ragdoc-backend
railway variable set OPENAI_API_KEY=<your-key> --service ragdoc-backend
railway variable set DATABASE_URL=<postgres-url> --service ragdoc-backend
```

### 2. Frontend Service
```bash
cd frontend
railway service create --name ragdoc-frontend
railway up --service ragdoc-frontend
railway variable set BACKEND_URL=https://<backend-url>.railway.app --service ragdoc-frontend
```

## Environment Variables

### Backend
| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |
| `OPENAI_API_KEY` | OpenAI API key for embeddings |
| `DATABASE_URL` | PostgreSQL connection URL |

### Frontend
| Variable | Description |
|---|---|
| `BACKEND_URL` | Full URL of the backend service (no trailing slash) |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/upload` | Upload PDF/TXT, chunk, embed, store |
| `POST` | `/api/query` | SSE stream: retrieve chunks → Claude answer |
| `GET` | `/api/health` | Health check |

## Architecture

```
Browser
  ├── POST /upload.php (PHP) → proxies to FastAPI /api/upload
  │     └── PyPDF2/text extraction → chunk (2000 chars) → OpenAI embed → pgvector store
  └── POST /api/query (FastAPI, direct SSE)
        └── embed question → pgvector cosine search → Claude stream → SSE tokens + citations
```
