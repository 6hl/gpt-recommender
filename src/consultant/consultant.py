import logging
from typing import Optional

from .agents import WebAgent
from .base_types import LocalArgs, ModelType, OpenAIArgs, Preference, Recommendations
from .cache import Cache
from .config import load_config
from .models import LocalModel, OpenAIModel
from .parsers import FilterRatings, GoodReadsParser, LetterboxdParser
from .prompts import (
    create_recommend_messages,
    create_summarizer_messages,
    create_web_search_messages,
)


class Consultant:

    def __init__(self, config_path: Optional[str] = None):
        self.config = load_config(config_path)
        self.config_path = config_path
        # TODO: add cache checks
        self.cache = Cache(bypass=(not self.config.performance.cache))
        self.model = self._load_model(self.config.model)

    def __call__(
        self, query: Optional[str] = None, skip_profile_recommendations: bool = False
    ):
        recommendations = Recommendations()
        if query is None:
            if self.config.recommender.type == "general":
                raise ValueError("Query is required for general recommendations.")
            query = f"Highly rated recent {self.config.recommender.type}"

        if self.config.recommender.web_search:
            recommendations.web = self._web_search(query)

        if (
            self.config.recommender.profile is not None
            and not self.config.recommender.type == "general"
            and not skip_profile_recommendations
        ):
            recommendations.profile = self._profile_recommendations()

        return recommendations

    def _load_model(self, model_args) -> LocalModel | OpenAIModel:
        if model_args.type == "local":
            model = LocalModel(model_args.path, model_args.device)
        elif model_args.type == "openai":
            model = OpenAIModel(model_args.api_key)
        else:
            raise ValueError(f"Unsupported model type: {model_args.type}")
        model.setup()
        return model

    def _create_model_args(
        self, messages: list[dict], **kwargs
    ) -> OpenAIArgs | LocalArgs:
        if self.config.model.type == ModelType.OPENAI:
            return OpenAIArgs(
                messages=messages,
                **kwargs,
            )
        else:
            return LocalArgs(messages=messages, **kwargs)

    def _query_model(
        self,
        messages: list[dict],
    ) -> str:
        model_args = self._create_model_args(messages)
        response = self.model.query(model_args)  # type: ignore
        parsed_response = self.model.parse_output(response)  # type: ignore
        return parsed_response

    def _web_search(self, query: str) -> str:
        # Perform web search and get recommendations
        sources = WebAgent.get_search_links(query, 5)
        logging.debug(f"Web search sources: {sources}")
        texts = [WebAgent.get_raw_document_body_from_link(source) for source in sources]
        messages = create_web_search_messages(texts)
        response = self._query_model(messages)
        logging.debug(f"Web search response: {response}")
        return response

    def _profile_recommendations(self, exclude_list: list[str] = []):
        rec_type = self.config.recommender.type
        if rec_type == "movies":
            reviews = GoodReadsParser.parse(user_id=self.config.recommender.profile)  # type: ignore
        elif rec_type == "books":
            reviews = LetterboxdParser.parse(user_id=self.config.recommender.profile)  # type: ignore
        else:
            raise ValueError(f"Unsupported recommendation type: {rec_type}")

        logging.debug(f"Parsed reviews: {reviews}")
        ratings = FilterRatings.collate_ratings(reviews)
        logging.debug(f"Filtered ratings: {ratings}")
        messages = create_summarizer_messages(rec_type, ratings)
        summary = self._query_model(messages)
        logging.debug(f"Summary: {summary}")

        preference = Preference(
            summary=summary,
            ratings=ratings,
            exclude_list=exclude_list,
        )
        messages = create_recommend_messages(rec_type, preference)
        recommendations = self._query_model(messages)
        logging.debug(f"Recommendations: {recommendations}")
        return recommendations

    def update_config(
        self,
        config: dict[str, str] | str,
        reset: bool = False,
    ) -> None:
        if reset:
            self.config = load_config(self.config.config_path)
            self.cache = Cache(bypass=(not self.config.performance.cache))
            self.model = self._load_model(self.config.model)
            return

        initial_model_args = (
            self.config.model.type,
            self.config.model.path,
            self.config.model.device,
            self.config.model.api_key,
        )
        for key, value in config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                logging.error(f"Invalid config key: {key}")
        self.cache = Cache(bypass=(not self.config.performance.cache))

        # prevent reloading the model if it is not changed
        if initial_model_args != (
            self.config.model.type,
            self.config.model.path,
            self.config.model.device,
            self.config.model.api_key,
        ):
            self.model = self._load_model(self.config.model)
