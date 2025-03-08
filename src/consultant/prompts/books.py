from .general import (
    USER_PREFERENCE_RECOMMEND_SYSTEM_PROMPT,
    USER_PREFERENCE_SUMMARIZER_SYSTEM_PROMPT,
)


def create_book_summarizer_system_prompt(n_recommendations: int = 5):
    return {
        "role": "system",
        "content": USER_PREFERENCE_SUMMARIZER_SYSTEM_PROMPT.format(
            category="books", n_recommendations=n_recommendations
        ),
    }


def create_book_recommend_system_prompt(n_recommendations: int = 5):
    return {
        "role": "system",
        "content": USER_PREFERENCE_RECOMMEND_SYSTEM_PROMPT.format(
            category="books", n_recommendations=n_recommendations
        ),
    }
