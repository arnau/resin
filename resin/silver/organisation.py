"""
Organisation transformation queries for the silver layer.
"""

from sqlalchemy import JSON, UUID, Insert, String, func, select, text
from sqlalchemy.dialects import postgresql as pg

from resin.bronze import schema as bronze
from resin.silver.schema import organisation, organisation_link


def organisation_raw():
    """Extract raw organisation data from bronze layer."""
    return (
        select(func.unnest(bronze.api_page.c.raw_data))
        .where(bronze.api_page.c.entity == "organisation")
        .cte("organisation_raw")
    )


def organisation_link_raw():
    """Extract organisation links from raw organisation data."""
    organisation_raw_cte = organisation_raw()

    return (
        select(
            func.cast(text("organisation->>'id'"), UUID).label("id"),
            func.cast(text("organisation->'links'->'link'"), pg.ARRAY(JSON)).label(
                "link"
            ),
        )
        .select_from(organisation_raw_cte)
        .cte("organisation_link_raw")
    )


def organisation_link_unnested():
    """Unnest organisation links."""
    organisation_link_raw_cte = organisation_link_raw()

    return (
        select(
            organisation_link_raw_cte.c.id,
            func.unnest(organisation_link_raw_cte.c.link).label("link"),
        )
        .select_from(organisation_link_raw_cte)
        .where(func.length(organisation_link_raw_cte.c.link) != 0)
        .cte("organisation_link_unnested")
    )


def organisation_link_selection():
    """Select specific fields from organisation links."""
    organisation_link_unnested_cte = organisation_link_unnested()

    return (
        select(
            organisation_link_unnested_cte.c.id,
            func.cast(text("link->>'href'"), String).label("href"),
            func.cast(text("link->>'rel'"), String).label("rel"),
        )
        .select_from(organisation_link_unnested_cte)
        .cte("organisation_link_selection")
    )


def organisation_link_select():
    """Transform organisation links into final format."""
    organisation_link_selection_cte = organisation_link_selection()

    return select(
        organisation_link_selection_cte.c.id.label("source_id"),
        func.array_extract(
            func.parse_path(organisation_link_selection_cte.c.href), -2
        ).label("target_entity"),
        func.cast(
            func.array_extract(
                func.parse_path(organisation_link_selection_cte.c.href), -1
            ),
            UUID,
        ).label("target_id"),
        organisation_link_selection_cte.c.href.label("href"),
        organisation_link_selection_cte.c.rel.label("relation_type"),
    ).where(organisation_link_selection_cte.c.rel != "ORCID_ID")


def organisation_select():
    """Transform raw organisation data into final format."""
    organisation_raw_cte = organisation_raw()

    return select(
        func.cast(text("organisation->>'id'"), UUID).label("id"),
        func.cast(text("organisation->>'name'"), String).label("name"),
    ).select_from(organisation_raw_cte)


def insert_organisation() -> Insert:
    """Insert statement for organisation table."""
    column_names = [col.name for col in organisation.columns]

    return organisation.insert().from_select(column_names, organisation_select())


def insert_organisation_link() -> Insert:
    """Insert statement for organisation link table."""
    column_names = [col.name for col in organisation_link.columns]
    return organisation_link.insert().from_select(
        column_names, organisation_link_select()
    )
