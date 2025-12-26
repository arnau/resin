"""
Bronze layer schema definitions for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sql import CreateTableIfNotExists
from . import api_entity, api_page, schema, tracker


def create_tables(conn: Connection) -> None:
    """Create all bronze tables using IF NOT EXISTS."""
    bronze_tables = [
        table for table in metadata.tables.values() if table.schema == "bronze"
    ]

    for table in bronze_tables:
        conn.execute(CreateTableIfNotExists(table))


__all__ = [
    "create_tables",
    "schema",
    "api_page",
    "api_entity",
    "tracker",
]
