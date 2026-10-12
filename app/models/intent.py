
from typing import Any, Literal

from pydantic import BaseModel, Field


class Intent(BaseModel):
    name: str = Field(
        description="Name of a registered action, or unknown."
    )
    parameters: dict[str, Any] = Field(default_factory=dict)
    needs_clarification: bool = False
    clarification_question: str | None = None


class ActionResult(BaseModel):
    status: Literal[
        "success",
        "clarification",
        "unsupported",
        "failed",
        "rejected",
    ]
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
