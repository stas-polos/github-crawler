"""Implementation of helper functions for logging."""

import logging
import sys

from settings import project_settings

FORMAT = "%(asctime)s [%(module)s] %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logger() -> None:
    """Configures the root logger and connects additional handlers depending on the settings."""
    settings = project_settings()
    handlers = [
        logging.StreamHandler(sys.stdout),
    ]
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True,
    )
