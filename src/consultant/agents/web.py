import random
import urllib.parse as parse
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from ..base_types import WebAgentSuggestedLink
from ..constants import COOKIE_INFORMATION, GOOGLE_SEARCH_BASE


class WebAgent:

    @staticmethod
    def get_search_links(
        text: str, num_requested_results: int
    ) -> list[WebAgentSuggestedLink]:
        """
        Retrieves search links based on a query text.
        """
        params = WebAgent.get_params(text, num_requested_results)
        resp = WebAgent._request(params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", class_="ezO2md")
        links = []
        for result in result_block:
            if not isinstance(result, Tag):
                continue
            link_tag = result.find("a", href=True)
            if not isinstance(link_tag, Tag):
                continue
            title_tag = link_tag.find("span", class_="CVA68e")
            description_tag = result.find("span", class_="FrIlee")

            if link_tag is not None and title_tag and description_tag:
                link = parse.unquote(
                    link_tag["href"].split("&")[0].replace("/url?q=", "")  # type: ignore[union-attr]
                )
                title = title_tag.text if title_tag else ""
                description = description_tag.text if description_tag else ""
                links.append(
                    WebAgentSuggestedLink(
                        link=link, title=title, description=description
                    )
                )
        return links

    @staticmethod
    def get_raw_document_body_from_link(link: WebAgentSuggestedLink) -> str:
        """
        Retrieves the raw document body from a WebAgentSuggestedLink.
        """
        # TODO: determine if there is a universal way to cleanup raw results
        resp = WebAgent._request(url=link.link)
        soup = BeautifulSoup(resp.text, "html.parser")
        body = soup.find("body")
        if body is None:
            return ""
        raw_page_text = body.get_text(separator="\n", strip=True)
        return raw_page_text

    @staticmethod
    def _request(
        url: str = GOOGLE_SEARCH_BASE,
        params: Optional[dict] = None,
        proxies: Optional[dict] = None,
        timeout: int = 5,
    ) -> requests.Response:
        resp = requests.get(
            url=url,
            headers=WebAgent._get_header(),
            params=params,
            proxies=proxies,
            timeout=timeout,
            verify=None,
            cookies=COOKIE_INFORMATION,
        )
        return resp

    @staticmethod
    def _generate_useragent() -> str:
        lynx_version = (
            f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
        )
        libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
        ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
        openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
        return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"

    @staticmethod
    def _get_header() -> dict[str, str]:
        return {"User-Agent": WebAgent._generate_useragent(), "Accept": "*/*"}

    @staticmethod
    def get_params(
        text: str, num_requested_results: int, result_start_index: int = 0
    ) -> dict[str, None | str | int]:
        return {
            "q": text,
            "num": num_requested_results,
            "hl": "en",
            "start": result_start_index,
            "safe": "active",
            "gl": None,
        }
