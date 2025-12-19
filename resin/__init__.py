"""
Resin: A package for fetching and processing GTR API data.
"""

from . import bronze, silver
from .metadata import metadata
from .sqlalchemy import CreateTableAs

__all__ = [
    "metadata",
    "CreateTableAs",
    "bronze",
    "silver",
]
