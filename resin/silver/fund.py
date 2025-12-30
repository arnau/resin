"""
Fund transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import fund
from resin.sql import (
    BigInteger,
    Insert,
    Uuid,
    fn,
    json_extract_as,
    json_extract_timestamp,
    select,
)


def _raw():
    """Extract raw fund data from bronze layer."""
    return (
        select(fn.unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "fund")
        .cte("raw")
    )


def _fieldset():
    """Transform raw fund data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            json_extract_as(raw_data, "$.id", Uuid).label("id"),
            json_extract_timestamp(raw_data, "$.start").label("start_date"),
            json_extract_timestamp(raw_data, "$.end").label("end_date"),
            json_extract_as(raw_data, "$.valuePounds.amount", BigInteger).label(
                "amount"
            ),
            fn.json_extract_string(raw_data, "$.valuePounds.currencyCode").label(
                "currency_code"
            ),
            fn.json_extract_string(raw_data, "$.category").label("category"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    """Select all fund records."""
    return select(_fieldset())


def insert_all() -> Insert:
    """Insert statement for fund table."""
    return fund.insert().from_select(list(fund.columns), _fieldset())
