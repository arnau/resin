"""
Resin: A package for fetching and processing GTR API data.
"""

from . import bronze, silver
from .fetcher import entity_mapping, fetch, get_total_pages, make_url
from .metadata import metadata
from .sqlalchemy import CreateTableAs

__all__ = [
    "fetch",
    "make_url",
    "get_total_pages",
    "entity_mapping",
    "metadata",
    "CreateTableAs",
    "bronze",
    "silver",
]
