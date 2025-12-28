"""
Artistic and creative product (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import artistic_and_creative_product
from resin.sql import (
    Uuid,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw artistic and creative product data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "artisticAndCreativeProduct")
        .cte("raw")
    )


def _fieldset():
    """Transform raw artistic and creative product data into final format."""
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
            pick(raw_data, "$.yearFirstProvided").label("year_first_provided"),
            pick(raw_data, "$.supportingUrl").label("supporting_url"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for artistic and creative product table."""
    return artistic_and_creative_product.insert().from_select(
        list(artistic_and_creative_product.columns), _fieldset()
    )
