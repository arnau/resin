"""
Silver layer transformations for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sqlalchemy import CreateTableIfNotExists
from . import organisation as org_mod
from . import person as person_mod
from . import schema

# Person accessors
person = person_mod.person_select()
insert_person = person_mod.insert_person()
person_link = person_mod.person_link_select()
insert_person_link = person_mod.insert_person_link()

# Organisation accessors
organisation = org_mod.organisation_select()
insert_organisation = org_mod.insert_organisation()
organisation_link = org_mod.organisation_link_select()
insert_organisation_link = org_mod.insert_organisation_link()


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
    "person",
    "person_link",
    "insert_person_link",
    "organisation_link",
    "insert_organisation_link",
    "schema",
]
