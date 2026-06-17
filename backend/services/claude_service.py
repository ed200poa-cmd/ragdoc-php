import os
import json
from typing import AsyncGenerator
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

_SYSTEM = (
    "You are a document Q&A assistant. Answer the user's question based ONLY on the "
    "provided context excerpts. If the answer is not in the context, say so clearly. "
    "Be concise and helpful."
)


def _get_llm() -> ChatAnthropic | None:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None
    return ChatAnthropic(
        model="claude-sonnet-4-6",
        anthropic_api_key=key,
        max_tokens=2048,
        streaming=True,
    )


async def stream_answer(
    question: str, chunks: list[dict]
) -> AsyncGenerator[str, None]:
    llm = _get_llm()
    if not llm:
        yield json.dumps({"token": "Error: ANTHROPIC_API_KEY is not configured."})
        return

    context = "\n\n---\n\n".join(
        f"[Source: {c['filename']}, chunk {c['chunk_index']}]\n{c['content']}"
        for c in chunks
    )

    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(
            content=f"Context from the document:\n\n{context}\n\nQuestion: {question}"
        ),
    ]

    async for chunk in llm.astream(messages):
        if chunk.content:
            yield json.dumps({"token": chunk.content})
