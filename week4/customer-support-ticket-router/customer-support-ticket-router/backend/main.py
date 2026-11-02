
import logging

from fastapi import FastAPI, HTTPException

from backend.llm_service import select_prompt_technique

from backend.schemas import (
    ClassifyRequest,
    ClassifyResponse,
    ErrorResponse,
)
from backend.llm_service import (
    classify_email,
    draft_reply,
    judge_reply,
    LLMConfigurationError,
)

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Customer Support Ticket Router",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "customer-support-ticket-router",
    }


@app.post(
    "/classify",
    response_model=ClassifyResponse,
    responses={
        400: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def classify(request: ClassifyRequest):
    email = request.email.strip()

    if len(email) < 5:
        raise HTTPException(
            status_code=400,
            detail="Please provide a longer support email.",
        )

    try:
       
        technique = select_prompt_technique(email)

        classification = classify_email(
            email,
            technique=technique,
        )

        reply = draft_reply(email, classification)
        judge = judge_reply(email, reply)

        return ClassifyResponse(
            classification=classification,
            draft_reply=reply,
            judge=judge,
            prompt_technique=technique,
        )

    except LLMConfigurationError as exc:
        logging.error("Ollama error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The language model is temporarily unavailable. "
                   "Check that Ollama is running.",
        ) from exc

    except ValueError as exc:
        logging.exception("Invalid request or prompt.")
        raise HTTPException(
            status_code=400,
            detail="The email could not be processed.",
        ) from exc

    except Exception as exc:
        logging.exception("Unexpected classification error.")
        raise HTTPException(
            status_code=503,
            detail="Could not process the email. Please try again.",
        ) from exc
