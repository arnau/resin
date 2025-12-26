"""
Schema definitions for the silver layer where data is cleaned and normalised.
"""

from ..metadata import metadata
from ..sql import (
    BigInteger,
    Column,
    DateTime,
    String,
    Table,
    Uuid,
)

link = Table(
    "link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("source_entity", Uuid(as_uuid=True)),
    Column("target_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("relation_type", String),
    schema="silver",
)

person = Table(
    "person",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("given_name", String),
    Column("family_name", String),
    Column("orcid_id", String),
    schema="silver",
)

person_link = Table(
    "person_link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("target_id", Uuid(as_uuid=True)),
    Column("href", String),
    Column("relation_type", String),
    schema="silver",
)

organisation = Table(
    "organisation",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("name", String),
    schema="silver",
)

organisation_link = Table(
    "organisation_link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("target_id", Uuid(as_uuid=True)),
    Column("href", String),
    Column("relation_type", String),
    schema="silver",
)


organisation_address = Table(
    "organisation_address",
    metadata,
    Column("organisation_id", Uuid(as_uuid=True)),
    Column("id", Uuid(as_uuid=True)),
    Column("line1", String),
    Column("line2", String),
    Column("line3", String),
    Column("line4", String),
    Column("line5", String),
    Column("city", String),
    Column("county", String),
    Column("post_code", String),
    Column("region", String),
    Column("country", String),
    Column("type", String),
    schema="silver",
)

fund = Table(
    "fund",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
    Column("amount", BigInteger),
    Column("currency_code", String),
    Column("category", String),
    schema="silver",
    # catalog="silver",
)

project = Table(
    "project",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("title", String),
    Column("status", String),
    Column("grant_category", String),
    Column("lead_funder", String),
    Column("lead_department", String),
    Column("abstract", String),
    Column("tech_abstract", String),
    Column("potential_impact", String),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
)

# TODO:
# project_identifier (raw_data->'identifiers'->'identifier')
# project_category ‣ select raw_data->>'id' id, raw_data->'healthCategories'->'healthCategory' health_cat, json_keys(raw_data) from raw limit 10;
# project_activity (raw_data->'researchActivities'->'researchActivity')
# project_subject (raw_data->'researchSubjects'->'researchSubject')
# project_topic (raw_data->'researchTopics'->'researchTopic')
# project_programme (raw_data->'rcukProgrammes'->'rcukProgramme')
# project_participant (raw_data->'participantValues'->'participant')
