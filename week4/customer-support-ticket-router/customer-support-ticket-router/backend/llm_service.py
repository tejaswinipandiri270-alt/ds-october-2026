
import json
import logging
import os
import urllib.error
import urllib.request

from pydantic import ValidationError

from backend.schemas import TicketClassification, JudgeScores
from backend.prompts import PROMPT_FUNCTIONS


logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
).rstrip("/")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")


class LLMConfigurationError(RuntimeError):
    """Raised when Ollama is unavailable or cannot process a request."""
    pass


def _call_ollama(messages: list[dict], json_mode: bool = False) -> str:
    """Send a chat request to Ollama."""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1},
    }

    if json_mode:
        payload["format"] = "json"

    request = urllib.request.Request(
        url=f"{OLLAMA_BASE_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))

        content = result.get("message", {}).get("content", "")

        if not isinstance(content, str) or not content.strip():
            raise LLMConfigurationError("Ollama returned an empty response.")

        return content.strip()

    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        logger.error("Ollama HTTP error %s: %s", exc.code, details)
        raise LLMConfigurationError(
            f"Ollama returned HTTP {exc.code}. Check the model and Ollama service."
        ) from exc

    except (urllib.error.URLError, TimeoutError) as exc:
        logger.exception("Could not connect to Ollama.")
        raise LLMConfigurationError(
            "Cannot connect to Ollama. Check that it is running."
        ) from exc

    except json.JSONDecodeError as exc:
        logger.exception("Ollama returned an invalid API response.")
        raise LLMConfigurationError(
            "Ollama returned an invalid API response."
        ) from exc


def _normalise_messages(prompt) -> list[dict]:
    """Support prompts represented as chat messages or plain text."""

    if isinstance(prompt, str):
        return [{"role": "user", "content": prompt}]

    if isinstance(prompt, list):
        return prompt

    raise ValueError("Prompt must be a string or a list of messages.")
def select_prompt_technique(email: str) -> str:
    """
    Use the LLM to understand the customer email and select
    a prompt technique automatically.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent customer-support routing assistant. "
                "Understand the meaning of the customer's email. "
                "Identify the main problem category and recommend a prompt "
                "technique for the downstream ticket-classification task. "
                "Do not select a category or technique using keywords alone. "
                "Consider the meaning and context of the complete email. "
                "Choose one category from: billing, technical, delivery, "
                "account, other. "
                "Choose one prompt_technique from: zero_shot, few_shot, "
                "role_based, chain_of_thought. "
                "Use these routing guidelines: "
                "zero_shot for straightforward requests; "
                "few_shot for requests that benefit from examples; "
                "role_based for issues needing a specialised support role; "
                "chain_of_thought for requests requiring multiple steps "
                "of analysis. "
                "Return only a valid JSON object containing category, "
                "prompt_technique, and reason. "
                "The reason must briefly explain your decision."
            ),
        },
        {
            "role": "user",
            "content": f"Customer email:\n{email}",
        },
    ]

    raw_output = _call_ollama(messages, json_mode=True)

    try:
        decision = json.loads(raw_output)

        category = decision["category"]
        technique = decision["prompt_technique"]
        reason = decision["reason"]

        allowed_categories = {
            "billing",
            "technical",
            "delivery",
            "account",
            "other",
        }

        if category not in allowed_categories:
            raise ValueError("Invalid category returned by the router.")

        if technique not in PROMPT_FUNCTIONS:
            raise ValueError("Invalid prompt technique returned by the router.")

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("The router did not provide a reason.")

        logger.info(
            "LLM router selected category=%s, technique=%s, reason=%s",
            category,
            technique,
            reason,
        )

        return technique

    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
        logger.warning(
            "LLM router returned an invalid response; retrying once: %s",
            exc,
        )

        retry_messages = messages + [
            {"role": "assistant", "content": raw_output},
            {
                "role": "user",
                "content": (
                    "Your previous response was invalid. Return one valid "
                    "JSON object containing category, prompt_technique, "
                    "and reason. Use only the allowed category and "
                    "technique values specified in the system instructions."
                ),
            },
        ]

        corrected_output = _call_ollama(
            retry_messages,
            json_mode=True,
        )

        decision = json.loads(corrected_output)

        category = decision["category"]
        technique = decision["prompt_technique"]
        reason = decision["reason"]

        if category not in {
            "billing",
            "technical",
            "delivery",
            "account",
            "other",
        }:
            raise ValueError("Invalid category returned by the router.")

        if technique not in PROMPT_FUNCTIONS:
            raise ValueError("Invalid prompt technique returned by the router.")

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("The router did not provide a reason.")

        logger.info(
            "LLM router selected category=%s, technique=%s",
            category,
            technique,
        )

        return technique


def _validate_classification(raw_output: str) -> TicketClassification:
    """Parse and validate the model's classification JSON."""

    return TicketClassification.model_validate_json(raw_output)


def classify_email(
    email: str,
    technique: str = "few_shot",
) -> TicketClassification:
    """Classify an email using a selected prompt technique and retry once."""

    if technique not in PROMPT_FUNCTIONS:
        raise ValueError(f"Unknown prompt technique: {technique}")

    messages = _normalise_messages(PROMPT_FUNCTIONS[technique](email))

    raw_output = _call_ollama(messages, json_mode=True)

    try:
        return _validate_classification(raw_output)

    except ValidationError as exc:
        logger.warning("Classification validation failed; retrying once: %s", exc)

    retry_messages = messages + [
        {"role": "assistant", "content": raw_output},
        {
            "role": "user",
            "content": (
                "Correct your previous JSON response to match the required schema. "
                "Allowed category values: billing, technical, delivery, account, other. "
                "Allowed priority values: low, medium, high. "
                "Allowed customer_wants values: refund, fix, information, cancel. "
                "Use the exact allowed values. Copy the product name only if it is "
                "explicitly mentioned in the email; otherwise use Unknown. "
                "Return one valid JSON object with no extra fields."
            ),
        },
    ]

    corrected_output = _call_ollama(retry_messages, json_mode=True)

    return _validate_classification(corrected_output)


def draft_reply(
    email: str,
    classification: TicketClassification,
) -> str:
    """Generate a polite customer-support reply with Ollama."""

    messages = [
        {
            "role": "system",
            "content": (
               "You are a professional customer-support agent. Write a concise, "
                "polite, empathetic reply that directly addresses the customer's actual issue. "
                "Use the customer's email and the provided classification to understand the problem. "
                "Explain a clear, practical next step the customer can take or the support team "
                "can take. If more information is needed, request only relevant, non-sensitive "
                "information through an appropriate support channel. "
                "Do not invent products, company policies, tracking results, dates, or actions. "
                "Do not claim that a tracking check, refund, repair, or cancellation has happened "
                 "unless the provided information confirms it. "
               "Do not promise an exact resolution time or delivery date without evidence. "
              "Never request passwords, one-time passcodes, or full payment-card details. "
               "Use the information available and do not repeat generic apologies unnecessarily. "
               "Return only the reply to the customer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Customer email:\n{email}\n\n"
                f"Classification:\n{classification.model_dump_json(indent=2)}\n\n"
                "Write the customer-support reply."
            ),
        },
    ]

    reply = _call_ollama(messages)

    if not reply:
        raise LLMConfigurationError("Ollama returned an empty draft reply.")

    return reply


def judge_reply(email: str, reply: str) -> JudgeScores:
    """Evaluate a reply using an LLM judge and a validated 1–5 rubric."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are an independent customer-support quality evaluator. "
                "Assess the draft reply against the original email. Return only JSON "
                "with integer fields question_answering_score, tone_score, "
                "policy_compliance_score, and a non-empty reason. Each score must "
                "be from 1 to 5. Question answering measures whether the main concern "
                "is addressed. Tone measures politeness, empathy, and professionalism. "
                "Policy compliance measures whether the reply avoids unsupported "
                "promises, invented actions, and unsafe commitments. Give a concise "
                "reason for the scores. Do not add extra fields."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Original customer email:\n{email}\n\n"
                f"Draft reply:\n{reply}\n\n"
                "Evaluate this reply using the rubric."
            ),
        },
    ]

    raw_output = _call_ollama(messages, json_mode=True)

    try:
        return JudgeScores.model_validate_json(raw_output)

    except ValidationError as exc:
        logger.warning("Judge validation failed; retrying once: %s", exc)

    retry_messages = messages + [
        {"role": "assistant", "content": raw_output},
        {
            "role": "user",
            "content": (
                "Correct your JSON. Include integer scores from 1 to 5 for "
                "question_answering_score, tone_score, and policy_compliance_score, "
                "plus a non-empty reason. Return only the required JSON object."
            ),
        },
    ]

    corrected_output = _call_ollama(retry_messages, json_mode=True)

    return JudgeScores.model_validate_json(corrected_output)
