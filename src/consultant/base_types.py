from typing import Optional

from pydantic import BaseModel, Field


class OpenAIArgs(BaseModel):
    messages: list[dict]
    max_completion_tokens: int = Field(
        1000, description="Maximum number of tokens to generate"
    )
    temperature: Optional[float] = Field(None, description="Sampling temperature")
    top_p: Optional[float] = Field(
        None, description="Nucleus sampling probability mass"
    )
    stop: list[str] | None = Field(None, description="List of stop sequences")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
