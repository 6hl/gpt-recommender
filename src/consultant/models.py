import os
from abc import ABC, abstractmethod
from typing import Optional

from openai.types.chat import ChatCompletionMessage

from .base_types import OpenAIArgs


class DefaultModel(ABC):

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def query(self, args):
        raise NotImplementedError

    @abstractmethod
    def parse_output(self, response):
        raise NotImplementedError


class OpenAIModel(DefaultModel):
    def __init__(
        self, api_key: Optional[str] = None, model: Optional[str] = "gpt-4o-mini"
    ):
        if api_key is None:
            try:
                api_key = os.environ["OPENAI_API_KEY"]
            except Exception as e:
                raise ValueError(
                    "Error retrieving API key from environment. Please set the OPENAI_API_KEY environment variable."
                ) from e
        self.api_key = api_key
        self.model = model

    def setup(self):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "Please install the OpenAI Python package with `pip install openai`."
            )

        self.client = OpenAI(api_key=self.api_key)

    def query(self, query: OpenAIArgs):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=query.messages,
                max_completion_tokens=query.max_completion_tokens,
                temperature=query.temperature,
                top_p=query.top_p,
                stop=query.stop,
                seed=query.seed,
            )
            return completion.choices[0].message
        except Exception as e:
            raise RuntimeError("Error during API call") from e

    def parse_output(self, response: ChatCompletionMessage):
        return response.content
