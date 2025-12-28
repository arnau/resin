"""
Dissemination (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import dissemination
from resin.sql import (
    Boolean,
    Uuid,
    fn,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw dissemination data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "dissemination")
        .cte("raw")
    )


def _fieldset():
    """Transform raw dissemination data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            pick(raw_data, "$.form").label("form"),
            pick(raw_data, "$.primaryAudience").label("primary_audience"),
            fn.split(pick(raw_data, "$.yearsOfDissemination"), ",").label(
                "years_of_dissemination"
            ),
            # pick(raw_data, "$.results").label("results"),
            pick(raw_data, "$.impact").label("impact"),
            pick(raw_data, "$.typeOfPresentation").label("presentation_type"),
            pick(raw_data, "$.geographicReach").label("geographic_reach"),
            pick_as(raw_data, "$.partOfOfficialScheme", Boolean).label(
                "part_of_official_scheme"
            ),
            pick(raw_data, "$.supportingUrl").label("supporting_url"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return dissemination.insert().from_select(list(dissemination.columns), _fieldset())
