"""
Tracker queries for bronze layer operations.
"""

from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.dialects import postgresql as pg

from . import schema


def entity_complete(entity: str, timestamp: datetime):
    """A query to mark an entity as complete."""
    return (
        update(schema.tracker)
        .where(schema.tracker.c.entity == entity)
        .values(status="complete", timestamp=timestamp)
    )


def entity_upsert(entity: str, page: int, total_pages: int | None = None):
    """A query to update progress for an entity, either by inserting a new record or updating an existing one."""
    values = dict(entity=entity, page=page, status="incomplete", timestamp=func.now())
    if total_pages is not None:
        values["total_pages"] = total_pages

    return (
        pg.insert(schema.tracker)
        .values(**values)
        .on_conflict_do_update(
            constraint=schema.tracker.primary_key,
            set_=dict(page=page, timestamp=func.now()),
        )
    )


def entity_total_pages(entity: str):
    """Query to get total pages for an entity from tracker."""
    return select(schema.tracker.c.total_pages).where(schema.tracker.c.entity == entity)


def entity_status(entity: str):
    """A query to get the current status for an entity."""
    return select(schema.tracker.c.page, schema.tracker.c.status).where(
        schema.tracker.c.entity == entity
    )
