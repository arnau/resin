"""
API page queries for bronze layer operations.
"""

from datetime import datetime

from sqlalchemy import JSON, Integer, func, literal, literal_column, select
from sqlalchemy.dialects import postgresql as pg

from . import schema


def entity_insert(entity_name: str, api_url: str, timestamp: datetime):
    """Build the insert query for storing API page data."""
    subquery = select(
        literal(timestamp.isoformat()).label("timestamp"),
        literal(entity_name).label("entity"),
        literal_column("page", type_=Integer),
        literal_column("totalPages", type_=Integer).label("total_pages"),
        literal_column(entity_name, type_=pg.ARRAY(JSON)).label("raw_data"),
    ).select_from(func.read_json(api_url))

    return schema.api_page.insert().from_select(list(schema.api_page.columns), subquery)


def entity_total_pages(entity: str):
    """Build query to get total pages for an entity."""
    return (
        select(schema.api_page.c.total_pages)
        .where(schema.api_page.c.entity == entity)
        .limit(1)
    )
