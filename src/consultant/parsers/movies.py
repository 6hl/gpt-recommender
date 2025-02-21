import requests
from bs4 import BeautifulSoup as bs

from ..constants import LETTERBOXD_USER_BASE, MAX_PAGES_TO_SCRAPE
from .default import DefaultParser

# pyright: reportIncompatibleMethodOverride=false


class LetterboxdParser(DefaultParser):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)...",
        "Accept-Language": "en-US, en;q=0.5",
    }

    @staticmethod
    def _parse_reviews(soup_response) -> list[dict]:
        # TODO: make parallel calls
        movie_reviews = []
        reviews = soup_response.select('[class="poster-container"]')
        for r in reviews:
            rating_str = LetterboxdParser._convert_rating(
                r.select('span[class*="rating"]')[0].text.strip()
            )
            title = r.select("img")[0]["alt"]
            movie_reviews.append({"rating": rating_str, "title": title})
        return movie_reviews

    @staticmethod
    def _request(url: str):
        res = requests.get(url, headers=LetterboxdParser.HEADERS)
        soup_response = bs(res.text, "html.parser")
        return soup_response

    @staticmethod
    def _convert_rating(rating_str: str) -> float:
        return sum(1 if c == "★" else 0.5 for c in rating_str)

    @staticmethod
    def parse(user_id: str):
        movie_reviews = []
        for i in range(1, MAX_PAGES_TO_SCRAPE + 1):
            movie_reviews += LetterboxdParser._parse_reviews(
                LetterboxdParser._request(
                    LETTERBOXD_USER_BASE.format(user_id=user_id, page_num=i)
                )
            )
        return movie_reviews
