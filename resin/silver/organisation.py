"""
Organisation transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import organisation
from resin.sql import Insert, Uuid, fn, json_extract_as, select


def _raw():
    """Extract raw organisation data from bronze layer."""
    return (
        select(fn.unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "organisation")
        .cte("raw")
    )


def _fieldset():
    """Transform raw organisation data into final format."""
    raw = _raw()

    return (
        select(
            json_extract_as(raw.c.raw_data, "$.id", Uuid).label("id"),
            fn.json_extract_string(raw.c.raw_data, "$.name").label("name"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    """Select all organisations."""
    return select(_fieldset())


def insert_all() -> Insert:
    """Insert statement for organisation table."""
    return organisation.insert().from_select(list(organisation.columns), _fieldset())
