"""
API page queries for bronze layer operations.
"""

from sqlalchemy import JSON, func, literal
from sqlalchemy.dialects import postgresql as pg

from . import schema


def entity_insert(entity_name: str, page: int, raw_data_json: str):
    """Insert query for storing raw JSON data."""
    return schema.api_page.insert().values(
        timestamp=func.now(),
        entity=entity_name,
        page=page,
        raw_data=func.cast(literal(raw_data_json), pg.ARRAY(JSON)),
    )
