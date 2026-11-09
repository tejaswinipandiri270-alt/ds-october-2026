
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.config import settings
from backend.rag.pipeline import RAGPipeline
from backend.services.ollama_client import generate_answer, OllamaError
from backend.dependencies import require_api_key


router = APIRouter()
_pipeline = None


def pipeline():
    global _pipeline

    if _pipeline is None:
        _pipeline = RAGPipeline()

    return _pipeline


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=settings.TOP_K, ge=1, le=20)
    history: list[dict] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    answer: str = Field(min_length=1, max_length=8000)
    rating: str = Field(pattern="^(helpful|not_helpful)$")
    comment: str = Field(default="", max_length=2000)


# Public health check
@router.get("/health")
def health():
    try:
        return {
            "status": "ok",
            "indexed_chunks": pipeline().store.count(),
            "ollama_model": settings.OLLAMA_MODEL
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {type(exc).__name__}"
        )


# Protected document ingestion
@router.post(
    "/ingest",
    dependencies=[Depends(require_api_key)]
)
def ingest():
    try:
        return {
            "status": "success",
            **pipeline().ingest_directory()
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Ingestion failed"
        ) from exc


# Protected document upload
@router.post(
    "/upload",
    dependencies=[Depends(require_api_key)]
)
async def upload(
    files: Annotated[list[UploadFile], File()]
):
    doc_dir = settings.path(settings.DOCUMENT_DIRECTORY)
    doc_dir.mkdir(parents=True, exist_ok=True)

    allowed = {".txt", ".pdf", ".docx"}
    max_size = settings.MAX_UPLOAD_MB * 1024 * 1024

    saved = []

    for item in files:
        suffix = Path(item.filename or "").suffix.lower()

        if suffix not in allowed:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {suffix}"
            )

        data = await item.read(max_size + 1)

        if len(data) > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"{item.filename} exceeds upload limit"
            )

        name = Path(item.filename or "upload").name
        destination = doc_dir / name

        destination.write_bytes(data)
        saved.append(name)

    try:
        result = pipeline().ingest_directory()

        return {
            "status": "success",
            "uploaded": saved,
            **result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed"
        ) from exc


# Protected retrieval
@router.post(
    "/retrieve",
    dependencies=[Depends(require_api_key)]
)
def retrieve(req: QueryRequest):
    try:
        return {
            "question": req.question,
            "results": pipeline().retrieve(
                req.question,
                req.top_k
            )
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Retrieval failed"
        ) from exc


# Protected RAG chat
@router.post(
    "/chat",
    dependencies=[Depends(require_api_key)]
)
def chat(req: QueryRequest):
    try:
        hits = pipeline().retrieve(
            req.question,
            req.top_k
        )

        answer = generate_answer(
            req.question,
            hits,
            history=req.history
        )

        sources = []
        seen = set()

        for hit in hits:
            meta = hit.get("metadata", {})
            key = (
                meta.get("filename"),
                meta.get("page")
            )

            if key not in seen:
                seen.add(key)

                sources.append({
                    "filename": meta.get("filename"),
                    "page": meta.get("page") or None,
                    "snippet": hit["text"][:450]
                })

        return {
            "answer": answer,
            "sources": sources
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except OllamaError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Chat request failed"
        ) from exc


# Protected feedback
@router.post(
    "/feedback",
    dependencies=[Depends(require_api_key)]
)
def feedback(req: FeedbackRequest):
    path = settings.path(settings.FEEDBACK_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    record = req.model_dump()
    record["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return {
        "status": "recorded"
    }
