"""
Organisation transformation queries for the silver layer.
"""

from sqlalchemy import JSON, UUID, Insert, String, func, select
from sqlalchemy.dialects import postgresql as pg

from .organisation import organisation_raw
from .schema import organisation_link


def organisation_link_raw():
    """Extract organisation links from raw organisation data."""
    organisation_raw_cte = organisation_raw()

    return (
        select(
            func.cast(
                func.json_extract_string(organisation_raw_cte.c.raw_data, "$.id"), UUID
            ).label("organisation_id"),
            func.unnest(
                func.cast(
                    func.json_extract_array(
                        organisation_raw_cte.c.raw_data, "$.links.link"
                    ),
                    pg.ARRAY(JSON),
                )
            ).label("link"),
        )
        .select_from(organisation_raw_cte)
        .cte("organisation_link_raw")
    )


def organisation_link_base():
    """Select specific fields from organisation links."""
    organisation_link_raw_cte = organisation_link_raw()

    return (
        select(
            organisation_link_raw_cte.c.organisation_id,
            func.cast(
                func.json_extract_string(organisation_link_raw_cte.c.link, "$.href"),
                String,
            ).label("href"),
            func.cast(
                func.json_extract_string(organisation_link_raw_cte.c.link, "$.rel"),
                String,
            ).label("rel"),
        )
        .select_from(organisation_link_raw_cte)
        .cte("organisation_link_base")
    )


def organisation_link_select():
    """Transform organisation links into final format."""
    organisation_link_base_cte = organisation_link_base()

    return select(
        organisation_link_base_cte.c.organisation_id.label("source_id"),
        func.array_extract(
            func.parse_path(organisation_link_base_cte.c.href), -2
        ).label("target_entity"),
        func.cast(
            func.array_extract(func.parse_path(organisation_link_base_cte.c.href), -1),
            UUID,
        ).label("target_id"),
        organisation_link_base_cte.c.href.label("href"),
        organisation_link_base_cte.c.rel.label("relation_type"),
    ).where(organisation_link_base_cte.c.rel != "ORCID_ID")


def organisation_link_insert() -> Insert:
    """Insert statement for organisation link table."""
    return organisation_link.insert().from_select(
        list(organisation_link.columns), organisation_link_select()
    )
