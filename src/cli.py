"""Implementation of loading all commands."""

import typer

from crawlers import searcher
from utils.logger import configure_logger


def bootstrap():
    """Loads all commands and runs application."""
    configure_logger()
    app = typer.Typer(name="App for parse github.com")
    app.add_typer(searcher.app, name="searcher")
    app()


if __name__ == "__main__":
    bootstrap()
