"""
API entity maps between the name of the entity (typically in singular form) and its API path, typically
in plural form and as a sub-resource for outcome entities.

This is a helper for normalising entities at query time, particularly when dealing with links.
"""

from resin.api_client import EntitySet

from ..sql import (
    ColumnElement,
    insert,
    select,
)
from .schema import api_entity


def insert_all(entities: EntitySet):
    """Insert query for API entity definitions."""
    values = [{"name": entity.name, "api_path": entity.api_path} for entity in entities]
    return insert(api_entity).values(values).on_conflict_do_nothing()


def entity_name(api_path: ColumnElement[str]):
    return (
        select(api_entity.c.name)
        .where(api_entity.c.api_path == api_path)
        .limit(1)
        .scalar_subquery()
    )


def entity_path(name: ColumnElement[str]):
    return (
        select(api_entity.c.api_path)
        .where(api_entity.c.name == name)
        .limit(1)
        .scalar_subquery()
    )
