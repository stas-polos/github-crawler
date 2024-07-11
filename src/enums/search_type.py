"""Implementation of the enumeration of the type objects which need search."""

from enum import Enum


class SearchType(str, Enum):
    """Enumeration of the type objects for search."""

    REPOSITORIES = "repositories"
    ISSUES = "issues"
    WIKIS = "wikis"
