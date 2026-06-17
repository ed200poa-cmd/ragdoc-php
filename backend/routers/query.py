import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from services.retrieval import retrieve_chunks
from services.claude_service import stream_answer

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    document_id: int


@router.post("/query")
async def query_document(
    req: QueryRequest,
    db: AsyncSession = Depends(get_session),
):
    chunks = await retrieve_chunks(req.question, req.document_id, db)

    async def event_stream():
        async for data in stream_answer(req.question, chunks):
            yield f"data: {data}\n\n"

        citations = [
            {
                "filename": c["filename"],
                "excerpt": c["content"][:200] + "..." if len(c["content"]) > 200 else c["content"],
                "similarity": round(c["similarity"], 3),
            }
            for c in chunks
        ]
        yield f"data: {json.dumps({'citations': citations})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/health")
async def health():
    return {"status": "ok"}
