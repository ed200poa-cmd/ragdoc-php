from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from services.embeddings import embed_text


async def retrieve_chunks(
    question: str, document_id: int, db: AsyncSession, top_k: int = 5
) -> list[dict]:
    embedding = await embed_text(question)
    embedding_str = "[" + ",".join(str(v) for v in embedding) + "]"

    result = await db.execute(
        text("""
            SELECT c.content, c.chunk_index, d.filename,
                   1 - (c.embedding <=> :emb::vector) AS similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.document_id = :doc_id
            ORDER BY c.embedding <=> :emb::vector
            LIMIT :top_k
        """),
        {"emb": embedding_str, "doc_id": document_id, "top_k": top_k},
    )

    return [
        {
            "content": row[0],
            "chunk_index": row[1],
            "filename": row[2],
            "similarity": float(row[3]),
        }
        for row in result.fetchall()
    ]
