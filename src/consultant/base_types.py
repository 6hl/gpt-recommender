from enum import Enum
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field


class ComparableEnum(Enum):
    """
    Base class to derive from for enums that can be compared to strings
    """

    def __str__(self):
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, ComparableEnum):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)


class RecommendType(ComparableEnum):
    BOOKS = "books"
    MOVIES = "movies"
    GENERAL = "general"


class ModelType(ComparableEnum):
    OPENAI = "openai"
    LOCAL = "local"


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


class LocalArgs(BaseModel):
    messages: list[dict[str, str]]
    max_tokens: int = Field(1000, description="Maximum number of tokens")
    temp: float = Field(0.7, description="Temperature")
    top_k: int = Field(40, description="Top K")
    min_p: float = Field(0.0, description="Minimum P")
    repeat_penalty: float = Field(1.18, description="Repeat penalty")
    repeat_last_n: int = Field(64, description="Repeat last N")
    n_batch: int = Field(8, description="Batch size")
    n_predict: Optional[int] = Field(None, description="Number of predictions")
    streaming: bool = Field(False, description="Streaming")


class WebAgentSuggestedLink(BaseModel):
    title: str
    link: str
    description: str


class Ratings(BaseModel):
    highest: pd.DataFrame
    lowest: pd.DataFrame
    recent: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True


class Preference(BaseModel):
    summary: str = ""
    ratings: Optional[Ratings] = None
    exclude_list: list[str] = []

    class Config:
        arbitrary_types_allowed = True


class ModelArgs(BaseModel):
    type: ModelType = Field(default=ModelType.LOCAL)
    path: str = Field(default="Phi-3-mini-4k-instruct.Q4_0.gguf")
    device: str = Field(default="cpu")
    api_key: Optional[str] = Field(
        default=None, description="API key for OpenAI or other services"
    )


class RecommenderArgs(BaseModel):
    type: RecommendType = Field(
        default=RecommendType.GENERAL,
        description="Type of recommendation (books, movies, general)",
    )
    web_search: bool = Field(
        default=True, description="Enable web search for recommendations"
    )
    n_recommendations: int = Field(
        default=5, description="Number of recommendations to return"
    )
    profile: Optional[str] = Field(
        default=None,
        description="User profile for personalized recommendations",
    )


class PerformanceArgs(BaseModel):
    cache: bool = Field(default=True, description="Enable caching for performance")


class Config(BaseModel):
    model: ModelArgs
    recommender: RecommenderArgs
    performance: PerformanceArgs


class Recommendations(BaseModel):
    web: Optional[str] = None
    profile: Optional[str] = None
