import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastembed import TextEmbedding

_model = TextEmbedding("BAAI/bge-small-en-v1.5")
_executor = ThreadPoolExecutor(max_workers=2)

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200
EMBEDDING_DIM = 384


def chunk_text(raw: str) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(raw):
        piece = raw[start : start + CHUNK_SIZE].strip()
        if piece:
            chunks.append(piece)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


async def embed_texts(texts: list[str]) -> list[list[float]]:
    loop = asyncio.get_event_loop()

    def _run() -> list[list[float]]:
        return [emb.tolist() for emb in _model.embed(texts)]

    return await loop.run_in_executor(_executor, _run)


async def embed_text(text: str) -> list[float]:
    results = await embed_texts([text])
    return results[0]
