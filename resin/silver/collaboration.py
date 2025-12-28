"""
Collaboration (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import collaboration
from resin.sql import (
    Uuid,
    pick,
    pick_as,
    pick_as_ts,
    select,
    unnest,
)


def _raw():
    """Extract raw project data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "collaboration")
        .cte("raw")
    )


def _fieldset():
    """Transform raw project data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.description").label("description"),
            pick(raw_data, "$.parentOrganisation").label("parent_organisation"),
            pick(raw_data, "$.childOrganisation").label("child_organisation"),
            pick(raw_data, "$.principalInvestigatorContribution").label(
                "principal_investigator_contribution"
            ),
            pick(raw_data, "$.partnerContribution").label("partner_contribution"),
            pick_as_ts(raw_data, "$.start").label("start_date"),
            pick_as_ts(raw_data, "$.end").label("end_date"),
            pick(raw_data, "$.sector").label("sector"),
            pick(raw_data, "$.country").label("country"),
            pick(raw_data, "$.impact").label("impact"),
            pick(raw_data, "$.supportingUrl").label("supporting_url"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for collaboration table."""
    return collaboration.insert().from_select(list(collaboration.columns), _fieldset())
