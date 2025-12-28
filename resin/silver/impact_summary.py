"""
Impact summary (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import impact_summary
from resin.sql import (
    Array,
    String,
    Uuid,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw impact summary data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "futherfunding")
        .cte("raw")
    )


def _fieldset():
    """Transform raw impact summary data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            pick_as(raw_data, "$.impactTypes.item", Array(String)).label(
                "impact_types"
            ),
            # pick(raw_data, "$.summary").label("summary"),
            # pick(raw_data, "$.beneficiaries").label("beneficiaries"),
            # pick(raw_data, "$.contributionMethod").label("contribution_method"),
            pick(raw_data, "$.sector").label(
                "sector"
            ),  # it's separated by commas but inconsistentl formatted
            pick(raw_data, "$.firstYearOfImpact").label(
                "first_year_of_impact"
            ),  # some values are 0 rather than null
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return impact_summary.insert().from_select(
        list(impact_summary.columns), _fieldset()
    )
