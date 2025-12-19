"""
Schema definitions for the silver layer where data is cleaned and normalised.
"""

from sqlalchemy import Column, String, Table, Uuid

from ..metadata import metadata

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
