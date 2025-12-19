"""
Person transformation queries for the silver layer.
"""

from sqlalchemy import JSON, UUID, Insert, String, func, select, text
from sqlalchemy.dialects import postgresql as pg

from resin.bronze import schema as bronze
from resin.silver.schema import person, person_link


def person_raw():
    """Extract raw person data from bronze layer."""
    return select(
        func.unnest(bronze.person.c.person).label("person"),
    ).cte("person_raw")


def person_link_raw():
    """Extract and unnest person links from raw person data."""
    person_raw_cte = person_raw()

    return (
        select(
            func.cast(text("person->>'id'"), UUID).label("id"),
            func.unnest(
                func.cast(text("person->'links'->'link'"), pg.ARRAY(JSON))
            ).label("link"),
        )
        .select_from(person_raw_cte)
        .cte("person_link_raw")
    )


def person_link_selection():
    """Select specific fields from person links."""
    person_link_raw_cte = person_link_raw()

    return (
        select(
            person_link_raw_cte.c.id,
            func.cast(text("link->>'href'"), String).label("href"),
            func.cast(text("link->>'rel'"), String).label("rel"),
        )
        .select_from(person_link_raw_cte)
        .cte("person_link_selection")
    )


def person_link_select():
    """Transform person links into final format."""
    person_link_selection_cte = person_link_selection()

    return select(
        person_link_selection_cte.c.id.label("source_id"),
        func.array_extract(func.parse_path(person_link_selection_cte.c.href), -2).label(
            "target_entity"
        ),
        func.cast(
            func.array_extract(func.parse_path(person_link_selection_cte.c.href), -1),
            UUID,
        ).label("target_id"),
        person_link_selection_cte.c.href.label("href"),
        person_link_selection_cte.c.rel.label("relation_type"),
    ).where(person_link_selection_cte.c.rel != "ORCID_ID")


def person_select():
    """Transform raw person data into final format."""
    person_raw_cte = person_raw()

    return select(
        func.cast(text("person->>'id'"), UUID).label("id"),
        func.cast(text("person->>'firstName'"), String).label("given_name"),
        func.cast(text("person->>'surname'"), String).label("family_name"),
        func.cast(text("person->>'orcidId'"), String).label("orcid_id"),
    ).select_from(person_raw_cte)


def insert_person() -> Insert:
    """Insert statement for person table."""
    column_names = [col.name for col in person.columns]

    return person.insert().from_select(column_names, person_select())


def insert_person_link() -> Insert:
    """Insert statement for person link table."""
    column_names = [col.name for col in person_link.columns]
    return person_link.insert().from_select(column_names, person_link_select())
