from pathlib import Path

import pytest
from requests import Response


@pytest.fixture()
def content(filepath: str | Path) -> bytes:
    with Path(filepath).open(mode="r", encoding="utf-8") as f:
        yield f.read().encode("utf-8")


@pytest.fixture()
def response(content: bytes, url: str) -> Response:
    response = Response()
    response.status_code = 200
    response.url = url
    response._content = content
    yield response
