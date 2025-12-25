"""
Fund transformation queries for the silver layer.
"""

from sqlalchemy import UUID, BigInteger, Insert, String, func, select

from resin.bronze import schema as bronze
from resin.silver.schema import fund
from resin.sqlalchemy import json_extract_as, json_extract_timestamp


def fund_raw():
    """Extract raw fund data from bronze layer."""
    return (
        select(func.unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "fund")
        .cte("fund_raw")
    )


def fund_select():
    """Transform raw fund data into final format."""
    fund_raw_ = fund_raw()
    raw_data = fund_raw_.c.raw_data

    return select(
        json_extract_as(raw_data, "$.id", UUID).label("id"),
        json_extract_timestamp(raw_data, "$.start").label("start_date"),
        json_extract_timestamp(raw_data, "$.end").label("end_date"),
        json_extract_as(raw_data, "$.valuePounds.amount", BigInteger).label("amount"),
        json_extract_as(raw_data, "$.valuePounds.currencyCode", String).label(
            "currency_code"
        ),
        json_extract_as(raw_data, "$.category", String).label("category"),
    ).select_from(fund_raw_)


def fund_insert() -> Insert:
    """Insert statement for fund table."""
    return fund.insert().from_select(list(fund.columns), fund_select())
