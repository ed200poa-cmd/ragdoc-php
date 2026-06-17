import os
from openai import AsyncOpenAI

_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200


def chunk_text(raw: str) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(raw):
        end = start + CHUNK_SIZE
        piece = raw[start:end].strip()
        if piece:
            chunks.append(piece)
        start = end - CHUNK_OVERLAP
    return chunks


async def embed_texts(texts: list[str]) -> list[list[float]]:
    response = await _client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


async def embed_text(text: str) -> list[float]:
    results = await embed_texts([text])
    return results[0]
