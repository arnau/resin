"""
Bronze layer schema definitions for the resin package.
"""

from sqlalchemy import ColumnElement, Connection, select

from ..api_client import EntitySet
from ..metadata import metadata
from ..sqlalchemy import CreateTableIfNotExists
from . import api_page, schema, tracker


def create_tables(conn: Connection) -> None:
    """Create all bronze tables using IF NOT EXISTS."""
    bronze_tables = [
        table for table in metadata.tables.values() if table.schema == "bronze"
    ]

    for table in bronze_tables:
        conn.execute(CreateTableIfNotExists(table))


def api_entity_insert(entities: EntitySet):
    """Create insert query for API entity definitions."""
    values = [{"name": entity.name, "api_path": entity.api_path} for entity in entities]
    return schema.api_entity.insert().values(values)


def lookup_entity_name(api_path: ColumnElement[str]):
    # TODO: Extract into bronze/api_entity.
    return (
        select(schema.api_entity.c.name)
        .where(schema.api_entity.c.api_path == api_path)
        .limit(1)
        .scalar_subquery()
    )


__all__ = [
    "create_tables",
    "api_entity_insert",
    "lookup_entity_name",
    "schema",
    "api_page",
    "tracker",
]
