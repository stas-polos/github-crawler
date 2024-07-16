# mypy: disable-error-code="call-arg"
"""Implementation of the global settings for project."""

from functools import lru_cache

from dotenv import find_dotenv
from pydantic import Extra, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Container with settings from virtual environment.

    Attributes:
        LOG_LEVEL: Logging level.

    """

    LOG_LEVEL: str = Field(..., env="LOG_LEVEL")

    class Config:
        """Configure for this container.

        Attributes:
            env_file (str): Path to env file.

        """

        env_file = find_dotenv(".env")
        extra = Extra.allow


@lru_cache
def project_settings():
    """Returns instance Settings."""
    return Settings()
