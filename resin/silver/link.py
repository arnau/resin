"""
Entity links. Links express a relationship between two entities.

The way the API expresses links means that most links are to be duplicated given that you should expect them to
be expressed in terms of both entities being the source entity.
"""

from resin.bronze import schema as bronze
from resin.bronze.api_entity import entity_name
from resin.sql import (
    ColumnElement,
    JsonArray,
    Uuid,
    fn,
    json_extract_as,
    path_extract,
    select,
)

from .schema import link


def _raw():
    """Extract raw data from bronze layer."""
    return select(
        bronze.api_page.c.entity,
        fn.unnest(bronze.api_page.c.raw_data).label("raw_data"),
    ).cte("raw")


def _link_raw():
    """Extract and unnest links."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            json_extract_as(raw_data, "$.id", Uuid).label("source_id"),
            raw.c.entity.label("source_entity"),
            fn.unnest(
                json_extract_as(raw_data, "$.links.link", JsonArray),
            ).label("link"),
        )
        .select_from(raw)
        .cte("link_raw")
    )


def _fieldset():
    """Select specific fields from links."""
    link_raw = _link_raw()

    return (
        select(
            link_raw.c.source_id,
            link_raw.c.source_entity,
            fn.json_extract_string(link_raw.c.link, "$.href").label("href"),
            fn.json_extract_string(link_raw.c.link, "$.rel").label("rel"),
        )
        .select_from(link_raw)
        .cte("fieldset")
    )


def extract_api_path(url: ColumnElement[str]):
    return fn.regexp_extract(url, "http://gtr.ukri.org/gtr/api/(.+)/", 1)


def _link():
    """Transform fund links into final format."""
    fieldset = _fieldset()

    return select(
        fieldset.c.source_id,
        fieldset.c.source_entity,
        fn.cast(
            path_extract(fieldset.c.href, -1),
            Uuid,
        ).label("target_id"),
        entity_name(extract_api_path(fieldset.c.href)).label("target_entity"),
        fieldset.c.rel.label("relation_type"),
    ).cte("link")


def select_all():
    return select(_link())


def insert_all():
    return link.insert().from_select(list(link.columns), _link())
