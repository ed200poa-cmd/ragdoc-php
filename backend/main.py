import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from models.database import init_db
from routers.upload import router as upload_router
from routers.query import router as query_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    anthropic = "set" if os.getenv("ANTHROPIC_API_KEY") else "NOT SET"
    openai = "set" if os.getenv("OPENAI_API_KEY") else "NOT SET"
    print(f"RAGDoc Backend — Anthropic: {anthropic} | OpenAI: {openai}")
    yield


app = FastAPI(
    title="RAGDoc — Document Q&A API",
    description="RAG-powered document Q&A backend with Claude + pgvector",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
