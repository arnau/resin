"""
Entity links. Links express a relationship between two entities.

The way the API expresses links means that most links are to be duplicated given that you should expect them to
be expressed in terms of both entities being the source entity.
"""

from sqlalchemy import JSON, UUID, ColumnElement, Insert, func, select
from sqlalchemy.dialects import postgresql as pg

from resin.bronze import schema as bronze
from resin.bronze.api_entity import entity_name
from resin.sqlalchemy import json_extract_as, path_extract

from .schema import link


def raw():
    """Extract raw data from bronze layer."""
    return select(
        bronze.api_page.c.entity,
        func.unnest(bronze.api_page.c.raw_data).label("raw_data"),
    ).cte("raw")


def link_raw():
    """Extract and unnest links."""
    raw_ = raw()
    raw_data = raw_.c.raw_data

    return (
        select(
            json_extract_as(raw_data, "$.id", UUID).label("source_id"),
            raw_.c.entity.label("source_entity"),
            func.unnest(
                json_extract_as(raw_data, "$.links.link", pg.ARRAY(JSON)),
            ).label("link"),
        )
        .select_from(raw_)
        .cte("link_raw")
    )


def link_fieldset():
    """Select specific fields from links."""
    link_raw_ = link_raw()

    return (
        select(
            link_raw_.c.source_id,
            link_raw_.c.source_entity,
            func.json_extract_string(link_raw_.c.link, "$.href").label("href"),
            func.json_extract_string(link_raw_.c.link, "$.rel").label("rel"),
        )
        .select_from(link_raw_)
        .cte("link_fieldset")
    )


def extract_api_path(url: ColumnElement[str]):
    return func.regexp_extract(url, "http://gtr.ukri.org/gtr/api/(.+)/", 1)


def link_select():
    """Transform fund links into final format."""
    link_fieldset_ = link_fieldset()

    link = select(
        link_fieldset_.c.source_id,
        link_fieldset_.c.source_entity,
        func.cast(
            path_extract(link_fieldset_.c.href, -1),
            UUID,
        ).label("target_id"),
        entity_name(extract_api_path(link_fieldset_.c.href)).label("target_entity"),
        link_fieldset_.c.rel.label("relation_type"),
    ).cte("link")

    return select(link)


def link_insert() -> Insert:
    """Insert statement from link selection."""
    return link.insert().from_select(list(link.columns), link_select())
