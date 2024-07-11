from pathlib import Path

import pytest
from furl import furl
from requests import Response

from crawlers import searcher
from enums import SearchType


def test_get_random_proxies_return_random_formatter_proxies() -> None:
    proxies = ["194.126.37.94:8080", "13.78.125.167:8080"]
    random_proxies = searcher.get_random_proxies(proxies)
    assert random_proxies["http"].startswith("http")
    assert random_proxies["https"].startswith("http")


def test_get_request_url_return_formatted_url_when_one_keyword() -> None:
    keyword = "nameç"
    url = searcher.get_request_url([keyword], SearchType.REPOSITORIES)

    f_url = furl(url)
    assert f_url.args["q"] == keyword
    assert f_url.args["type"] == SearchType.REPOSITORIES


def test_get_request_url_return_formatted_url_when_two_keywords() -> None:
    keywords = ["key1", "key2"]
    url = searcher.get_request_url(keywords, SearchType.REPOSITORIES)

    f_url = furl(url)
    assert f_url.args["q"] == "key1 OR key2"
    assert f_url.args["type"] == SearchType.REPOSITORIES


@pytest.mark.parametrize(
    "filepath, url",
    [
        (
            Path(Path.cwd() / "./tests/fixtures/search.html"),
            "https://github.com/search?q=python+OR+docker&type=repositories&p=2",
        )
    ],
)
def test_get_urls_return_expected_results(response: Response) -> None:
    urls = searcher.get_urls(response)
    assert urls == [
        {"url": "https://github.com/jupyter/docker-stacks"},
        {"url": "https://github.com/codefresh-contrib/python-flask-sample-app"},
        {"url": "https://github.com/sous-chefs/docker"},
        {"url": "https://github.com/kubernetes-client/python"},
        {"url": "https://github.com/joyzoursky/docker-python-chromedriver"},
        {"url": "https://github.com/janza/docker-python3-opencv"},
        {"url": "https://github.com/docker-training/webapp"},
        {"url": "https://github.com/Show-Me-the-Code/python"},
        {"url": "https://github.com/phusion/passenger-docker"},
        {"url": "https://github.com/docker-library/docker"},
    ]


@pytest.mark.parametrize(
    "filepath, url", [(Path(Path.cwd() / "./tests/fixtures/detail.html"), "https://github.com/docker-library/docker")]
)
def test_get_detail_information_changed_url(response: Response) -> None:
    url = {"url": "https://github.com/docker-library/docker"}
    searcher.get_detail_information(response, url)
    assert url == {
        "url": "https://github.com/docker-library/docker",
        "extra": {
            "owner": "docker-library",
            "language_stats": {
                "Shell": 70.9,
                "Dockerfile": 24.9,
                "jq": 4.2,
            },
        },
    }
