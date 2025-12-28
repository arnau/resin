"""
Spinout (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import spinout
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
        .where(bronze.api_page.c.entity == "spinOut")
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
            pick(raw_data, "$.description").label("description"),
            pick(raw_data, "$.companyName").label("company_name"),
            # pick(raw_data, "$.companyDescription").label("company_description"),
            pick(raw_data, "$.impact").label("impact"),
            pick(raw_data, "$.website").label("website"),
            pick(raw_data, "$.registrationNumber").label("registration_number"),
            pick(raw_data, "$.yearEstablished").label("year_established"),
            # pick(raw_data, "$.ipExploited").label("ip_exploited"),
            # pick(raw_data, "$.jointVenture").label("joint_venture"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return spinout.insert().from_select(list(spinout.columns), _fieldset())
