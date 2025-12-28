"""
Further funding (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import further_funding
from resin.sql import (
    BigInteger,
    Uuid,
    pick,
    pick_as,
    pick_as_ts,
    select,
    unnest,
)


def _raw():
    """Extract raw further funding data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "futherfunding")
        .cte("raw")
    )


def _fieldset():
    """Transform raw further funding data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            # pick(raw_data, "$.narrative").label("narrative"),
            pick_as(raw_data, "$.amount.amount", BigInteger).label("amount"),
            pick(raw_data, "$.amount.currencyCode").label("currency_code"),
            pick(raw_data, "$.organisation").label("organisation"),
            pick(raw_data, "$.department").label("department"),
            pick(raw_data, "$.fundingId").label("funding_id"),
            pick_as_ts(raw_data, "$.start").label("start_date"),
            pick_as_ts(raw_data, "$.end").label("end_date"),
            pick(raw_data, "$.sector").label("sector"),
            pick(raw_data, "$.country").label("country"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return further_funding.insert().from_select(
        list(further_funding.columns), _fieldset()
    )
