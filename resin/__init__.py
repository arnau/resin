"""
Resin: A package for fetching and processing GTR API data.
"""

from .fetcher import entity_mapping, fetch, get_total_pages, make_url

__all__ = ["fetch", "make_url", "get_total_pages", "entity_mapping"]
