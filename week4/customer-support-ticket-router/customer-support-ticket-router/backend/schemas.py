
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Allowed ticket categories
Category = Literal[
    "billing",
    "technical",
    "delivery",
    "account",
    "other",
]

# Allowed priority levels
Priority = Literal[
    "low",
    "medium",
    "high",
]

# What the customer wants
CustomerWants = Literal[
    "refund",
    "fix",
    "information",
    "cancel",
]

# Available prompt techniques
PromptTechnique = Literal[
    "zero_shot",
    "few_shot",
    "role_based",
    "chain_of_thought",
]


# Structured ticket classification returned by the LLM
class TicketClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Category
    priority: Priority
    product: str = Field(
        min_length=1,
        max_length=120,
        description="Product or service mentioned, or 'Unknown'.",
    )
    customer_wants: CustomerWants


# LLM-as-judge scores for the drafted reply
class JudgeScores(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_answering_score: int = Field(ge=1, le=5)
    tone_score: int = Field(ge=1, le=5)
    policy_compliance_score: int = Field(ge=1, le=5)
    reason: str = Field(min_length=1, max_length=1000)


# Request received by the FastAPI endpoint
class ClassifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=5, max_length=10000)
    prompt_technique: PromptTechnique = "few_shot"


# Successful response returned by the API
class ClassifyResponse(BaseModel):
    classification: TicketClassification
    draft_reply: str
    judge: JudgeScores
    prompt_technique: PromptTechnique


# Error response structure
class ErrorResponse(BaseModel):
    detail: str
