"""
Project transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import project
from resin.sql import (
    Uuid,
    fn,
    json_extract_as,
    json_extract_timestamp,
    select,
)


def _raw():
    """Extract raw project data from bronze layer."""
    return (
        select(fn.unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "project")
        .cte("raw")
    )


def _fieldset():
    """Transform raw project data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            json_extract_as(raw_data, "$.id", Uuid).label("id"),
            fn.json_extract_string(raw_data, "$.title").label("title"),
            fn.json_extract_string(raw_data, "$.status").label("status"),
            fn.json_extract_string(raw_data, "$.grantCategory").label("grant_category"),
            fn.json_extract_string(raw_data, "$.leadFunder").label("lead_funder"),
            fn.json_extract_string(raw_data, "$.leadOrganisationDepartment").label(
                "lead_department"
            ),
            fn.json_extract_string(raw_data, "$.abstractText").label("abstract"),
            fn.json_extract_string(raw_data, "$.techAbstractText").label(
                "tech_abstract"
            ),
            fn.json_extract_string(raw_data, "$.potentialImpact").label(
                "potential_impact"
            ),
            json_extract_timestamp(raw_data, "$.start").label("start_date"),
            json_extract_timestamp(raw_data, "$.end").label("end_date"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select(_fieldset())


def insert_all():
    """Insert statement for fund table."""
    return project.insert().from_select(list(project.columns), _fieldset())
