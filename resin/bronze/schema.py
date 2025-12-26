"""
The bronze layer reflects the raw data from the GTR API.
"""

from ..metadata import metadata
from ..sql import (
    Column,
    DateTime,
    Integer,
    JsonArray,
    String,
    Table,
    fn,
)

tracker = Table(
    "tracker",
    metadata,
    Column("entity", String, primary_key=True),
    Column("page", Integer),
    Column("status", String),
    Column("total_pages", Integer),
    Column("timestamp", DateTime, default=fn.current_timestamp()),
    schema="bronze",
)

api_page = Table(
    "api_page",
    metadata,
    Column("timestamp", DateTime, default=fn.current_timestamp()),
    Column("entity", String, primary_key=True),
    Column("page", Integer, primary_key=True),
    Column("raw_data", JsonArray),
    schema="bronze",
)

api_entity = Table(
    "api_entity",
    metadata,
    Column("name", String, primary_key=True),
    Column("api_path", String, nullable=False),
    schema="bronze",
)
