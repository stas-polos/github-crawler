"""Crawler for GitHub search parsing."""

import json
import logging
import random
import threading
from typing import Any

import requests
import typer
from furl import furl
from lxml.html import fromstring
from requests import Response

from enums import SearchType

logger = logging.getLogger(__name__)


app = typer.Typer(name="GitHub Crawler")


def get_random_proxies(proxies: list[str]) -> dict[str, str]:
    """Returns random proxies for requests.

    Args:
        proxies (list[str]): List of proxies to use.

    Returns:
        dict[str, str]: Dictionary of random proxies.

    """
    proxy = random.choice(proxies)
    if not proxy.startswith("http"):
        proxy = f"http://{proxy}"
    return {"http": proxy, "https": proxy}


def get_request_url(keywords: list[str], type_: SearchType) -> str:
    """Returns formatted url to github search.

    Args:
        keywords (list[str]): List of keywords to search.
        type_ (SearchType): Type of search.

    Returns:
        str: Formatted url to github search.

    """
    f_url = furl("https://github.com/search")
    f_url.add(
        args={
            # query param for search by keyword
            "q": " OR ".join(f"{k}" for k in keywords),
            # query param for search by type
            "type": type_,
        }
    )
    logger.debug(f"Formatted url: {f_url.tostr()}")
    return f_url.tostr()


def get_urls(response: Response) -> list[dict[str, str]]:
    """Returns extracted urls from response.

    Args:
        response (Response): Response from github search.

    Returns:
        list[dict[str, str]]: List of extracted urls.

    """
    base_url = furl(response.url).origin
    tree = fromstring(response.text)

    hrefs: list[str] = tree.xpath("//div[contains(@class, 'search-title')]/a/@href")
    return [{"url": furl(base_url).add(path=href).tostr()} for href in hrefs]


def get_detail_information(response: Response, url: dict[str, Any]) -> None:
    """Returns detail information about repos.

    Args:
        response (Response): Response of repos detail page.
        url (dict[str, Any]): Url of repos detail page.

    """
    owner = furl(response.url).path.segments[0]
    stats = {}

    tree = fromstring(response.text)
    for lang in tree.xpath("//h2[contains(text(), 'Languages')]/following-sibling::ul/li/a"):
        name, stat = lang.xpath("./span/text()")
        stats[name.strip()] = float(stat.strip().replace("%", ""))

    url["extra"] = {"owner": owner, "language_stats": stats or None}


def processing_detail_page(session: requests.Session, url: dict[str, Any]) -> None:
    """Makes requests to detail page and parse it.

    Args:
        session (requests.Session): Requests session.
        url (dict[str, Any]): Url to detail page.

    """
    detail_response = session.get(url=url["url"])
    get_detail_information(detail_response, url)


def search(task: dict[str, Any]) -> list[dict[str, Any]]:
    """Starts the search process in GitHub."""
    session = requests.Session()
    session.headers.update(
        {
            "accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            )
        }
    )
    session.proxies = get_random_proxies(task["proxies"])

    search_response = session.get(url=get_request_url(task["keywords"], task["type"]))
    urls = get_urls(search_response)

    if task["type"] == SearchType.REPOSITORIES:
        threads = []
        for url in urls:
            thread = threading.Thread(target=processing_detail_page, args=(session, url))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    return urls


@app.command(
    name="crawl",
    help="This command launches the crawler for parsing GitHub searches.",
)
def run_search(
    keywords: list[str] = typer.Option(..., help="A list of keywords to be used as search terms."),
    proxies: list[str] = typer.Option(..., help="A list of proxies to be used as search terms."),
    search_type: SearchType = typer.Option(..., help="The type of search to perform."),
):
    """Launches the crawler for parsing GitHub searches."""
    task = {
        "keywords": keywords,
        "proxies": proxies,
        "type": search_type,
    }
    logger.debug(f"Input task: {json.dumps(task, indent=2, ensure_ascii=False)}")
    result = search(task)
    logger.info(f"Search results: {json.dumps(result, indent=2, ensure_ascii=False)}")
