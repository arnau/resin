"""
Tracker queries for bronze layer operations.
"""

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects import postgresql as pg

from . import schema


def entity_complete(entity: str, timestamp: datetime):
    """A query to mark an entity as complete."""
    return (
        update(schema.tracker)
        .where(schema.tracker.c.entity == entity)
        .values(status="complete", timestamp=timestamp)
    )


def entity_upsert(entity: str, page: int, timestamp: datetime):
    """A query to update progress for an entity, either by inserting a new record or updating an existing one."""
    return (
        pg.insert(schema.tracker)
        .values(page=page, entity=entity, status="incomplete", timestamp=timestamp)
        .on_conflict_do_update(
            constraint=schema.tracker.primary_key,
            set_=dict(page=page),
        )
    )


def entity_status(entity: str):
    """A query to get the current status for an entity."""
    return select(schema.tracker.c.page, schema.tracker.c.status).where(
        schema.tracker.c.entity == entity
    )
