"""
Silver layer transformations for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sqlalchemy import CreateTableIfNotExists
from . import organisation, schema
from .fund import fund_insert, fund_select
from .fund_link import fund_link_insert, fund_link_select
from .organisation import organisation_insert, organisation_select
from .organisation_address import (
    organisation_address_insert,
    organisation_address_select,
)
from .organisation_link import organisation_link_insert, organisation_link_select
from .person import person_insert, person_select
from .person_link import person_link_insert, person_link_select


def create_tables(conn: Connection) -> None:
    """Create all silver tables using IF NOT EXISTS."""
    silver_tables = [
        table for table in metadata.tables.values() if table.schema == "silver"
    ]

    for table in silver_tables:
        conn.execute(CreateTableIfNotExists(table))


__all__ = [
    "create_tables",
    "organisation",
    "organisation_select",
    "organisation_insert",
    "person",
    "person_select",
    "person_insert",
    "person_link_select",
    "person_link_insert",
    "organisation_link_select",
    "organisation_link_insert",
    "organisation_address_select",
    "organisation_address_insert",
    "fund_select",
    "fund_insert",
    "fund_link_select",
    "fund_link_insert",
    "schema",
]
