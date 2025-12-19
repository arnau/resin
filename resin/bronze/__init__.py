"""
Bronze layer schema definitions for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sqlalchemy import CreateTableIfNotExists
from . import schema


def create_tables(conn: Connection) -> None:
    """Create all bronze tables using IF NOT EXISTS."""
    bronze_tables = [
        table for table in metadata.tables.values() if table.schema == "bronze"
    ]

    for table in bronze_tables:
        conn.execute(CreateTableIfNotExists(table))


__all__ = ["create_tables", "schema"]
