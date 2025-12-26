"""
Silver layer transformations for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sql import CreateTableIfNotExists
from . import (
    fund,
    link,
    organisation,
    organisation_address,
    person,
    project,
    schema,
)


def create_tables(conn: Connection) -> None:
    """Create all silver tables using IF NOT EXISTS."""
    silver_tables = [
        table for table in metadata.tables.values() if table.schema == "silver"
    ]

    for table in silver_tables:
        conn.execute(CreateTableIfNotExists(table))


__all__ = [
    "create_tables",
    "fund",
    "organisation",
    "organisation_address",
    "person",
    "link",
    "project",
    "schema",
]
