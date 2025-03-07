from typing import Optional

USER_PREFERENCE_SUMMARIZER_SYSTEM_PROMPT = """You are a helpful assistant that summarizes the users taste in {category} based on their reviews.
You will be provided three sets of reviews:
- The user's most recently rated {category}.
- The user's highest rated {category}.
- The user's lowest rated {category}.

Each will be given a rating 1-5, where 5 is the highest rating (really enjoyed by the user).

Your task is to summarize the users taste in {category} based on these reviews.
Respond with a list of three sentences and be concise. Use the following format:
- The user's preferences based on the most recently rated {category}.
- The user's preferences based on the highest rated {category}.
- The user's preferences based on the lowest rated {category}."""


USER_PREFERENCE_SUMMARIZER_USER_PROMPT = """# Most recently rated
{recently_rated}

# Highest rated
{highest_rated}

# Lowest rated
{lowest_rated}
"""


USER_PREFERENCE_RECOMMEND_SYSTEM_PROMPT = """You are a helpful assistant that gives recommendations.

You will be provided the following:
- A summary of the user's taste in {category}.
- A list of {category} and ratings in table format that the user has already rated.
- A list of {category} to exclude from recommending.

You will respond by giving a numbered list of recommendations for the user based off of their preferences.
Do not add commentary and only respond with a numbered list of {n_recommendations} recommendations."""


USER_PREFERENCE_RECOMMEND_USER_PROMPT = """# Summary of the user's taste
{summary}

# List of ratings
{rating_list}

# List to exclude from recommending
{exclude_list}
"""


def format_summarizer_user_prompt(
    recently_rated: str, highest_rated: str, lowest_rated: str
):
    return {
        "role": "user",
        "content": USER_PREFERENCE_SUMMARIZER_USER_PROMPT.format(
            recently_rated=recently_rated,
            highest_rated=highest_rated,
            lowest_rated=lowest_rated,
        ),
    }


def format_preference_user_prompt(
    summary: str, rating_list: str, exclude_list: Optional[str] = ""
) -> dict:
    return {
        "role": "user",
        "content": USER_PREFERENCE_RECOMMEND_USER_PROMPT.format(
            summary=summary,
            rating_list=rating_list,
            exclude_list=exclude_list,
        ),
    }
