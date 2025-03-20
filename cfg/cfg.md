# Creating a config

### Creating a config yaml takes three main fields:

```python
class Config(BaseModel):
    model: ModelArgs
    recommender: RecommenderArgs
    performance: PerformanceArgs
```

### Each of these three can have the following fields:

```python
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
```


### Here is an example:
```yaml
model:
  type: openai
recommender:
  web_search: true
  n_recommendations: 5
performance:
  cache: true
```
> can select model type, note `openai` requires setting up a `.env` file in the base folder with `OPENAI_API_KEY=<your-key>`