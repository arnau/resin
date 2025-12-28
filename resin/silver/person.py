"""
Person transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import person
from resin.sql import Insert, Uuid, fn, json_extract_as, select


def _raw():
    """Extract raw person data from bronze layer."""
    return (
        select(fn.unnest(bronze.api_page.c.raw_data))
        .where(bronze.api_page.c.entity == "person")
        .cte("raw")
    )


def _fieldset():
    """Transform raw person data into final format."""
    raw = _raw()

    return (
        select(
            json_extract_as(raw.c.value, "$.id", Uuid).label("id"),
            fn.json_extract_string(raw.c.value, "$.firstName").label("given_name"),
            fn.json_extract_string(raw.c.value, "$.surname").label("family_name"),
            fn.json_extract_string(raw.c.value, "$.orcidId").label("orcid_id"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    """Select all person records."""
    return select(_fieldset())


def person_insert() -> Insert:
    """Insert statement for person table."""
    return person.insert().from_select(list(person.columns), _fieldset())
