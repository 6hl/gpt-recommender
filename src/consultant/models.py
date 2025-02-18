import os
from abc import ABC, abstractmethod
from typing import Optional

from .base_types import LocalArgs, OpenAIArgs
from .formatter import format_local_response


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

    def parse_output(self, response):
        return response.content


class LocalModel(DefaultModel):

    def __init__(self, model_path: str, device: Optional[str] = "kompute"):
        self.model_path = model_path
        self.model_name = os.path.basename(model_path)
        self.device = device

    def setup(self):
        try:
            from gpt4all import GPT4All
        except ImportError:
            raise ImportError(
                "Please install the gpt4all library with `pip install gpt4all`."
            )

        self.model = GPT4All(self.model_path, device=self.device)

    def query(self, query: LocalArgs):
        message = format_local_response(query.messages, self.model_name)
        try:
            response = self.model.generate(
                message,
                max_tokens=query.max_tokens,
                temp=query.temp,
                top_k=query.top_k,
                min_p=query.min_p,
                repeat_penalty=query.repeat_penalty,
                repeat_last_n=query.repeat_last_n,
                n_batch=query.n_batch,
                n_predict=query.n_predict,
                streaming=query.streaming,
            )
            return response
        except Exception as e:
            raise e

    def parse_output(self, response: str):
        return response
