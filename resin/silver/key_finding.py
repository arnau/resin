"""
Key finding (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import key_finding
from resin.sql import (
    Array,
    String,
    Uuid,
    list_trim,
    pick,
    pick_as,
    select,
    unnest,
)


def _raw():
    """Extract raw data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "keyFinding")
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
            # pick(raw_data, "$.nonAcademicUses").label("non_academic_uses"),
            pick(raw_data, "$.exploitationPathways").label("exploitation_pathways"),
            list_trim(pick_as(raw_data, "$.sectors.item", Array(String))).label(
                "sectors"
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
    return key_finding.insert().from_select(list(key_finding.columns), _fieldset())
