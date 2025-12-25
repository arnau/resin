"""
Organisation transformation queries for the silver layer.
"""

from sqlalchemy import UUID, Insert, String, func, select

from resin.bronze import schema as bronze
from resin.silver.schema import organisation


def organisation_raw():
    """Extract raw organisation data from bronze layer."""
    return (
        select(func.unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "organisation")
        .cte("organisation_raw")
    )


def organisation_select():
    """Transform raw organisation data into final format."""
    organisation_raw_cte = organisation_raw()

    return select(
        func.cast(
            func.json_extract_string(organisation_raw_cte.c.raw_data, "$.id"), UUID
        ).label("id"),
        func.cast(
            func.json_extract_string(organisation_raw_cte.c.raw_data, "$.name"), String
        ).label("name"),
    ).select_from(organisation_raw_cte)


def organisation_insert() -> Insert:
    """Insert statement for organisation table."""
    return organisation.insert().from_select(
        list(organisation.columns), organisation_select()
    )
