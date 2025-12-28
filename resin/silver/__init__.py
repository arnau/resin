"""
Silver layer transformations for the resin package.
"""

from sqlalchemy import Connection

from ..metadata import metadata
from ..sql import CreateTableIfNotExists
from . import (
    artistic_and_creative_product,
    collaboration,
    dissemination,
    fund,
    further_funding,
    impact_summary,
    intellectual_property,
    key_finding,
    link,
    organisation,
    organisation_address,
    person,
    policy_influence,
    product,
    project,
    publication,
    research_database_and_model,
    research_material,
    schema,
    software_and_technical_product,
    spinout,
)


def create_tables(conn: Connection) -> None:
    """Create all silver tables using IF NOT EXISTS."""
    silver_tables = [
        table for table in metadata.tables.values() if table.schema == "silver"
    ]

    for table in silver_tables:
        conn.execute(CreateTableIfNotExists(table))


__all__ = [
    "artistic_and_creative_product",
    "collaboration",
    "create_tables",
    "dissemination",
    "fund",
    "further_funding",
    "impact_summary",
    "intellectual_property",
    "key_finding",
    "link",
    "organisation",
    "organisation_address",
    "person",
    "policy_influence",
    "product",
    "project",
    "publication",
    "research_database_and_model",
    "research_material",
    "schema",
    "software_and_technical_product",
    "spinout",
]
