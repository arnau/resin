"""
Policy influence (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import policy_influence
from resin.sql import (
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
        .where(bronze.api_page.c.entity == "policyInfluence")
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
            pick(raw_data, "$.influence").label("influence"),
            pick(raw_data, "$.type").label("type"),
            pick(raw_data, "$.guidelineTitle").label("guideline_title"),
            pick(raw_data, "$.impact").label("impact"),
            # pick(raw_data, "$.methods").label("methods"),
            # list_trim(pick_as(raw_data, "$.areas.item", Array(String))).label("areas"),
            pick(raw_data, "$.geographicReach").label("geographic_reach"),
            pick(raw_data, "$.supportingUrl").label("supporting_url"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return policy_influence.insert().from_select(
        list(policy_influence.columns), _fieldset()
    )
