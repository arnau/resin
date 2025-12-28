"""
Intellectual property (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import intellectual_property
from resin.sql import (
    Uuid,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw intellectual property data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "intellectualProperty")
        .cte("raw")
    )


def _fieldset():
    """Transform raw intellectual property data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            pick(raw_data, "$.protection").label("protection"),
            pick(raw_data, "$.patentId").label("patent_id"),
            pick(raw_data, "$.yearProtectionGranted").label("year_protection_granted"),
            # pick(raw_data, "$.type").label("type"),
            pick(raw_data, "$.impact").label("impact"),
            pick(raw_data, "$.licensed").label("licensed"),
            # pick(raw_data, "$.patentUrl").label("patent_url"),
            # pick_as_ts(raw_data, "$.start").label("start_date"),
            # pick_as_ts(raw_data, "$.end").label("end_date"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return intellectual_property.insert().from_select(
        list(intellectual_property.columns), _fieldset()
    )
