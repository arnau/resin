"""
Schema definitions for the silver layer where data is cleaned and normalised.
"""

from sqlalchemy import UUID, Column, String, Table

from ..metadata import metadata

person = Table(
    "person",
    metadata,
    Column("id", UUID),
    Column("given_name", String),
    Column("family_name", String),
    Column("orcid_id", String),
)

person_link = Table(
    "person_link",
    metadata,
    Column("source_id", UUID),
    Column("target_entity", String),
    Column("target_id", UUID),
    Column("href", String),
    Column("relation_type", String),
)

organisation = Table(
    "organisation",
    metadata,
    Column("id", UUID),
    Column("name", String),
)

organisation_link = Table(
    "organisation_link",
    metadata,
    Column("source_id", UUID),
    Column("target_entity", String),
    Column("target_id", UUID),
    Column("href", String),
    Column("relation_type", String),
)
