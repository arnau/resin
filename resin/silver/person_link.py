"""
Person transformation queries for the silver layer.
"""

from sqlalchemy import JSON, UUID, Insert, String, func, select
from sqlalchemy.dialects import postgresql as pg

from .person import person_raw
from .schema import person_link


def person_link_raw():
    """Extract and unnest person links from raw person data."""
    person_raw_cte = person_raw()

    return (
        select(
            func.cast(
                func.json_extract_string(person_raw_cte.c.person, "id"), UUID
            ).label("source_id"),
            func.unnest(
                func.cast(
                    func.json_extract_string(person_raw_cte.c.person, "links->link"),
                    pg.ARRAY(JSON),
                )
            ).label("link"),
        )
        .select_from(person_raw_cte)
        .cte("person_link_raw")
    )


def person_link_base():
    """Select specific fields from person links."""
    person_link_raw_cte = person_link_raw()

    return (
        select(
            person_link_raw_cte.c.source_id,
            func.cast(
                func.json_extract_string(person_link_raw_cte.c.link, "href"), String
            ).label("href"),
            func.cast(
                func.json_extract_string(person_link_raw_cte.c.link, "rel"), String
            ).label("rel"),
        )
        .select_from(person_link_raw_cte)
        .cte("person_link_base")
    )


def person_link_select():
    """Transform person links into final format."""
    person_link_base_cte = person_link_base()

    return select(
        person_link_base_cte.c.source_id,
        func.array_extract(func.parse_path(person_link_base_cte.c.href), -2).label(
            "target_entity"
        ),
        func.cast(
            func.array_extract(func.parse_path(person_link_base_cte.c.href), -1),
            UUID,
        ).label("target_id"),
        person_link_base_cte.c.href.label("href"),
        person_link_base_cte.c.rel.label("relation_type"),
    ).where(person_link_base_cte.c.rel != "ORCID_ID")


def person_link_insert() -> Insert:
    """Insert statement for person link table."""
    return person_link.insert().from_select(
        list(person_link.columns), person_link_select()
    )
