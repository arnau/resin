"""
Research material (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import research_material
from resin.sql import (
    Boolean,
    Uuid,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "researchMaterial")
        .cte("raw")
    )


def _fieldset():
    """Transform raw data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            pick(raw_data, "$.type").label("type"),
            pick(raw_data, "$.impact").label("impact"),
            # pick(raw_data, "$.softwareDeveloped").label("software_developed"),
            # pick(raw_data, "$.softwareOpenSourced").label("software_open_sourced"),
            pick_as(raw_data, "$.providedToOthers", Boolean).label(
                "provided_to_others"
            ),
            pick(raw_data, "$.yearFirstProvided").label("year_first_provided"),
            pick(raw_data, "$.supportingUrl").label("supporting_url"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return research_material.insert().from_select(
        list(research_material.columns), _fieldset()
    )
