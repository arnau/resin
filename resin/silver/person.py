"""
Person transformation queries for the silver layer.
"""

from sqlalchemy import UUID, Insert, String, func, select

from resin.bronze import schema as bronze
from resin.silver.schema import person


def person_raw():
    """Extract raw person data from bronze layer."""
    return (
        select(func.unnest(bronze.api_page.c.raw_data))
        .where(bronze.api_page.c.entity == "person")
        .cte("person_raw")
    )


def person_select():
    """Transform raw person data into final format."""
    person_raw_cte = person_raw()

    return select(
        func.cast(func.json_extract_string(person_raw_cte.c.value, "$.id"), UUID).label(
            "id"
        ),
        func.cast(
            func.json_extract_string(person_raw_cte.c.value, "$.firstName"), String
        ).label("given_name"),
        func.cast(
            func.json_extract_string(person_raw_cte.c.value, "$.surname"), String
        ).label("family_name"),
        func.cast(
            func.json_extract_string(person_raw_cte.c.value, "$.orcidId"), String
        ).label("orcid_id"),
    ).select_from(person_raw_cte)


def person_insert() -> Insert:
    """Insert statement for person table."""
    return person.insert().from_select(list(person.columns), person_select())
