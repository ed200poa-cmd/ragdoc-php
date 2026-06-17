import io
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session, Document, Chunk
from services.embeddings import chunk_text, embed_texts

try:
    import PyPDF2
    _HAS_PDF = True
except ImportError:
    _HAS_PDF = False

router = APIRouter()


def _extract_text(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".pdf") and _HAS_PDF:
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return content.decode("utf-8", errors="replace")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    content = await file.read()
    extracted = _extract_text(file.filename, content)

    if not extracted.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    doc = Document(filename=file.filename)
    db.add(doc)
    await db.flush()

    chunks = chunk_text(extracted)
    if not chunks:
        raise HTTPException(status_code=400, detail="Document produced no text chunks")

    embeddings = await embed_texts(chunks)

    for i, (chunk_content, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(Chunk(
            document_id=doc.id,
            content=chunk_content,
            chunk_index=i,
            embedding=embedding,
        ))

    await db.commit()

    return {
        "success": True,
        "document_id": doc.id,
        "filename": file.filename,
        "chunk_count": len(chunks),
    }
