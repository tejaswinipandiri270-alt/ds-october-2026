

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated
from langfuse import Langfuse
from time import perf_counter

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)
from pydantic import BaseModel, Field

from backend.config import settings
from backend.rag.pipeline import RAGPipeline
from backend.services.ollama_client import (
    generate_answer,
    OllamaError
)
from backend.dependencies import require_api_key
from backend.services.azure_blob_service import AzureBlobService
from backend.services.azure_indexer_service import AzureIndexerService


router = APIRouter()

langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_BASE_URL
)
_pipeline = None


# --------------------------------------------------
# RAG PIPELINE INITIALIZATION
# --------------------------------------------------

def pipeline():
    global _pipeline

    if _pipeline is None:
        _pipeline = RAGPipeline()

    return _pipeline


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=settings.TOP_K, ge=1, le=20)
    history: list[dict] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    answer: str = Field(min_length=1, max_length=8000)
    rating: str = Field(pattern="^(helpful|not_helpful)$")
    comment: str = Field(default="", max_length=2000)


# --------------------------------------------------
# PUBLIC HEALTH CHECK
# --------------------------------------------------

@router.get("/health")
def health():

    try:
        rag = pipeline()

        indexed_chunks = (
            rag.store.count()
            if rag.store is not None
            else None
        )

        return {
            "status": "ok",

            "llm_provider": settings.LLM_PROVIDER,

            "chat_model": (
                settings.FOUNDRY_CHAT_DEPLOYMENT
                if settings.LLM_PROVIDER.lower() == "foundry"
                else settings.OLLAMA_MODEL
            ),

            "retrieval_provider": (
                "azure_ai_search"
                if settings.AZURE_SEARCH_ENABLED
                else "local_chromadb"
            ),

            "local_indexed_chunks": indexed_chunks
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {type(exc).__name__}: {exc}"
        ) from exc


# --------------------------------------------------
# PROTECTED DOCUMENT INGESTION
# --------------------------------------------------

@router.post(
    "/ingest",
    dependencies=[Depends(require_api_key)]
)
def ingest():

    try:

        if settings.AZURE_SEARCH_ENABLED:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Azure mode uses Blob Storage and "
                    "Azure AI Search for document ingestion. "
                    "Use the /upload endpoint."
                )
            )

        return {
            "status": "success",
            **pipeline().ingest_directory()
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Ingestion failed"
        ) from exc


# --------------------------------------------------
# PROTECTED DOCUMENT UPLOAD
# --------------------------------------------------

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

    # 1. Validate and save uploaded documents

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

        result = None
        azure_result = None

        # 2. Local ChromaDB ingestion

        if not settings.AZURE_SEARCH_ENABLED:

            result = pipeline().ingest_directory()

        # 3. Azure Blob Storage and AI Search ingestion

        else:

            blob_service = AzureBlobService()

            for name in saved:

                destination = doc_dir / name

                blob_service.upload_file(
                    file_path=destination,
                    blob_name=name
                )

            # Trigger Azure AI Search indexer

            indexer_service = AzureIndexerService()

            try:

                azure_result = indexer_service.run_indexer()

            except Exception as exc:

                if (
                    "Another indexer invocation is currently in progress"
                    in str(exc)
                ):

                    azure_result = {
                        "indexer": "rag-1794563417722-indexer",
                        "status": "already_running",
                        "message": (
                            "Documents uploaded to Blob Storage. "
                            "Indexer is processing."
                        )
                    }

                else:
                    raise

        return {
            "status": "success",
            "uploaded": saved,
            "local_ingestion": result,
            "azure_ingestion": azure_result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(exc)}"
        ) from exc


# --------------------------------------------------
# PROTECTED DOCUMENT RETRIEVAL
# --------------------------------------------------

@router.post(
    "/retrieve",
    dependencies=[Depends(require_api_key)]
)
def retrieve(req: QueryRequest):

    try:

        results = pipeline().retrieve(
            req.question,
            req.top_k
        )

        return {
            "question": req.question,
            "results": results
        }

    except RuntimeError as exc:

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {str(exc)}"
        ) from exc


# --------------------------------------------------
# PROTECTED RAG CHAT
# --------------------------------------------------



@router.post(
    "/chat",
    dependencies=[Depends(require_api_key)]
)
def chat(req: QueryRequest):

    try:
        # Start total request timer
        request_start = perf_counter()

        # 1. Start the main Langfuse trace
        with langfuse.start_as_current_observation(
            as_type="span",
            name="nexus-it-chat",
            input={
                "question": req.question,
                "top_k": req.top_k
            }
        ) as trace:

            # 2. Retrieve relevant documents
            with langfuse.start_as_current_observation(
                as_type="span",
                name="document-retrieval",
                input={
                    "question": req.question,
                    "top_k": req.top_k
                }
            ) as retrieval_span:

                retrieval_start = perf_counter()

                hits = pipeline().retrieve(
                    req.question,
                    req.top_k
                )

                retrieval_latency_ms = round(
                    (perf_counter() - retrieval_start) * 1000,
                    2
                )

                retrieval_span.update(
                    output={
                        "retrieved_documents": len(hits),
                        "retrieval_latency_ms": retrieval_latency_ms,
                        "source_titles": [
                            hit.get("title")
                            or (hit.get("metadata") or {}).get("filename")
                            or "unknown"
                            for hit in hits
                        ]
                    }
                )

            # 3. Generate grounded answer
            with langfuse.start_as_current_observation(
                as_type="span",
                name="answer-generation",
                input={
                    "question": req.question,
                    "provider": settings.LLM_PROVIDER
                }
            ) as generation_span:

                
            # 3. Generate grounded answer
             
            # 3. Generate grounded answer and monitor with Langfuse
           # 3. Generate grounded answer and monitor with Langfuse
           # 3. Generate grounded answer and monitor with Langfuse

                    
            # 3. Generate grounded answer and monitor with Langfuse

              generation_start = perf_counter()

            with langfuse.start_as_current_observation(
                as_type="generation",
                name="answer-generation",
                input={
                    "question": req.question,
                    "provider": settings.LLM_PROVIDER
                },
                model=settings.FOUNDRY_CHAT_DEPLOYMENT
            ) as generation_span:

                generation_result = generate_answer(
                    req.question,
                    hits,
                    history=req.history
                )

                answer = generation_result["answer"]
                usage = generation_result["usage"]
                model_name = generation_result["model"]
                provider = generation_result["provider"]

                generation_latency_ms = round(
                    (perf_counter() - generation_start) * 1000,
                    2
                )

                generation_span.update(
                    model=model_name,
                    output={
                        "answer": answer,
                        "generation_latency_ms": generation_latency_ms,
                        "provider": provider
                    },
                    usage_details={
                        "input": usage["input_tokens"],
                        "output": usage["output_tokens"],
                        "total": usage["total_tokens"]
                    }
                )



            # 4. Prepare source information
            sources = []
            seen = set()

            for hit in hits:

                metadata = hit.get("metadata") or {}

                filename = (
                    hit.get("title")
                    or metadata.get("filename")
                    or "unknown"
                )

                page = metadata.get("page")
                key = (filename, page)

                if key not in seen:

                    seen.add(key)

                    sources.append({
                        "filename": filename,
                        "page": page or None,
                        "snippet": hit.get("text", "")[:450]
                    })

            # 5. Calculate total request latency
            total_latency_ms = round(
                (perf_counter() - request_start) * 1000,
                2
            )

            # 6. Update main Langfuse trace
            trace.update(
                output={
                    "answer": answer,
                    "source_count": len(sources),
                    "retrieved_documents": len(hits),

                    "retrieval_latency_ms": retrieval_latency_ms,
                    "generation_latency_ms": generation_latency_ms,
                    "total_latency_ms": total_latency_ms,

                    "model": model_name,
                    "provider": provider,
                    "input_tokens": usage["input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "total_tokens": usage["total_tokens"]
                }
            )

            # 7. Flush Langfuse observations
            langfuse.flush()

            # 8. Return normal API response
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
            detail=f"Chat request failed: {str(exc)}"
        ) from exc

# --------------------------------------------------
# PROTECTED FEEDBACK
# --------------------------------------------------

@router.post(
    "/feedback",
    dependencies=[Depends(require_api_key)]
)
def feedback(req: FeedbackRequest):

    path = settings.path(settings.FEEDBACK_FILE)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = req.model_dump()

    record["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    with path.open("a", encoding="utf-8") as f:

        f.write(
            json.dumps(record) + "\n"
        )

    return {
        "status": "recorded"
    }
