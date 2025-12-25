"""
The bronze layer reflects the raw data from the GTR API.
"""

from sqlalchemy import JSON, Column, DateTime, Integer, String, Table
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.sql import func

from ..metadata import metadata

tracker = Table(
    "tracker",
    metadata,
    Column("entity", String, primary_key=True),
    Column("page", Integer),
    Column("status", String),
    Column("total_pages", Integer),
    Column("timestamp", DateTime, default=func.current_timestamp()),
    schema="bronze",
)

api_page = Table(
    "api_page",
    metadata,
    Column("timestamp", DateTime, default=func.current_timestamp()),
    Column("entity", String, primary_key=True),
    Column("page", Integer, primary_key=True),
    Column("raw_data", pg.ARRAY(JSON)),
    schema="bronze",
)

api_entity = Table(
    "api_entity",
    metadata,
    Column("name", String, primary_key=True),
    Column("api_path", String, nullable=False),
    schema="bronze",
)
