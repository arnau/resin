"""
Fund links.
"""

from sqlalchemy import JSON, UUID, ColumnElement, Insert, func, literal, select
from sqlalchemy.dialects import postgresql as pg

from resin.bronze import lookup_entity_name
from resin.sqlalchemy import json_extract_as, path_extract

from .fund import fund_raw
from .schema import link


def fund_link_raw():
    """Extract and unnest fund links."""
    fund_raw_ = fund_raw()
    raw_data = fund_raw_.c.raw_data

    return (
        select(
            json_extract_as(raw_data, "$.id", UUID).label("source_id"),
            literal("fund").label("source_entity"),
            func.unnest(
                json_extract_as(raw_data, "$.links.link", pg.ARRAY(JSON)),
            ).label("link"),
        )
        .select_from(fund_raw_)
        .cte("link_raw")
    )


def fund_link_base():
    """Select specific fields from links."""
    link_raw = fund_link_raw()

    return (
        select(
            link_raw.c.source_id,
            link_raw.c.source_entity,
            func.json_extract_string(link_raw.c.link, "$.href").label("href"),
            func.json_extract_string(link_raw.c.link, "$.rel").label("rel"),
        )
        .select_from(link_raw)
        .cte("link_base")
    )


def extract_api_path(url: ColumnElement[str]):
    return func.regexp_extract(url, "http://gtr.ukri.org/gtr/api/(.+)/", 1)


def fund_link_select():
    """Transform fund links into final format."""
    link_base = fund_link_base()

    link = select(
        link_base.c.source_id,
        link_base.c.source_entity,
        func.cast(
            path_extract(link_base.c.href, -1),
            UUID,
        ).label("target_id"),
        lookup_entity_name(extract_api_path(link_base.c.href)).label("target_entity"),
        link_base.c.rel.label("relation_type"),
    ).cte("link")

    return select(link)


def fund_link_insert() -> Insert:
    return link.insert().from_select(list(link.columns), fund_link_select())
