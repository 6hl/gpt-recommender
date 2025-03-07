from ..base_types import Preference, Ratings, RecommendType
from .books import (
    create_book_recommend_system_prompt,
    create_book_summarizer_system_prompt,
)
from .general import create_preference_user_prompt, create_summarizer_user_prompt
from .movies import (
    create_film_recommend_system_prompt,
    create_film_summarizer_system_prompt,
)

_summarizer_func_map = {
    RecommendType.BOOKS: create_book_summarizer_system_prompt,
    RecommendType.MOVIES: create_film_summarizer_system_prompt,
}

_preference_func_map = {
    RecommendType.BOOKS: create_book_recommend_system_prompt,
    RecommendType.MOVIES: create_film_recommend_system_prompt,
}


def create_summarizer_messages(
    recommend_type: RecommendType, ratings: Ratings, n_recommendations: int = 5
):
    return [
        _summarizer_func_map[recommend_type](n_recommendations=n_recommendations),
        create_summarizer_user_prompt(
            recently_rated=ratings.recent.to_markdown(),  # type: ignore
            highest_rated=ratings.highest.to_markdown(),  # type: ignore
            lowest_rated=ratings.lowest.to_markdown(),  # type: ignore
        ),
    ]


def create_recommend_messages(
    recommend_type: RecommendType, preference: Preference, n_recommendations: int = 5
):
    return [
        _preference_func_map[recommend_type](n_recommendations=n_recommendations),
        create_preference_user_prompt(
            preference.summary,
            preference.ratings.recent.to_markdown(),  # type: ignore
            preference.exclude_list,
        ),
    ]
