import math
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup as bs

from ..constants import GOOD_READS_USER_BASE

# pyright: reportIncompatibleMethodOverride=false


class DefaultParser(ABC):

    @abstractmethod
    def parse(self):
        raise NotImplementedError


class GoodReadsParser(DefaultParser):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)...",
        "Accept-Language": "en-US, en;q=0.5",
    }

    @staticmethod
    def _parse_reviews(soup_response) -> list[dict]:
        # TODO: make parallel calls
        books_reviews = []
        reviews = soup_response.select('[class="bookalike review"]')
        for r in reviews:
            title = r.select("[class='field title']")[0].get_text()[13:].strip()
            author = (
                r.select("[class='field author']")[0]
                .get_text()[6:]
                .strip()
                .split("\n")[0]
            )
            rating = r.select("[class='staticStars notranslate']")[0].get_text().strip()
            books_reviews.append({"title": title, "author": author, "rating": rating})
        return books_reviews

    @staticmethod
    def _request(url: str):
        res = requests.get(url, headers=GoodReadsParser.HEADERS)
        soup_response = bs(res.text, "html.parser")
        return soup_response

    @staticmethod
    def parse(user_id: str):

        initial_request = GoodReadsParser._request(
            GOOD_READS_USER_BASE.format(user_id=user_id, page_num=1)
        )
        book_reviews = GoodReadsParser._parse_reviews(initial_request)
        page_info = (
            initial_request.select("div[class='inter loading uitext']")[-1]
            .text.strip()
            .split(" ")
        )
        n_pages = math.ceil(int(page_info[2]) / int(page_info[0]))

        for i in range(2, n_pages + 1):
            book_reviews += GoodReadsParser._parse_reviews(
                GoodReadsParser._request(
                    GOOD_READS_USER_BASE.format(user_id=user_id, page_num=i)
                )
            )
        return book_reviews
