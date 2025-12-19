"""
The bronze layer reflects the raw data from the GTR API.
"""

from sqlalchemy import JSON, Column, Table
from sqlalchemy.dialects import postgresql as pg

from ..metadata import metadata

person = Table(
    "person_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("person", JSON),
    schema="bronze",
)
organisation = Table(
    "organisation_raw",
    metadata,
    Column("organisation", JSON),
    schema="bronze",
)
