"""
The bronze layer reflects the raw data from the GTR API.
"""

from sqlalchemy import JSON, Column, DateTime, Integer, String, Table
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.sql import func

from ..metadata import metadata

fund = Table(
    "fund_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("fund", pg.ARRAY(JSON)),
    schema="bronze",
)

project = Table(
    "project_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("project", pg.ARRAY(JSON)),
    schema="bronze",
)

person = Table(
    "person_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("person", pg.ARRAY(JSON)),
    schema="bronze",
)

organisation = Table(
    "organisation_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("organisation", pg.ARRAY(JSON)),
    schema="bronze",
)

artisticandcreativeproduct = Table(
    "artisticandcreativeproduct_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("artisticandcreativeproduct", pg.ARRAY(JSON)),
    schema="bronze",
)

collaboration = Table(
    "collaboration_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("collaboration", pg.ARRAY(JSON)),
    schema="bronze",
)

dissemination = Table(
    "dissemination_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("dissemination", pg.ARRAY(JSON)),
    schema="bronze",
)

futherfunding = Table(
    "futherfunding_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("futherfunding", pg.ARRAY(JSON)),
    schema="bronze",
)

impactsummary = Table(
    "impactsummary_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("impactsummary", pg.ARRAY(JSON)),
    schema="bronze",
)

intellectualproperty = Table(
    "intellectualproperty_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("intellectualproperty", pg.ARRAY(JSON)),
    schema="bronze",
)

keyfinding = Table(
    "keyfinding_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("keyfinding", pg.ARRAY(JSON)),
    schema="bronze",
)

policyinfluence = Table(
    "policyinfluence_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("policyinfluence", pg.ARRAY(JSON)),
    schema="bronze",
)

product = Table(
    "product_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("product", pg.ARRAY(JSON)),
    schema="bronze",
)

researchdatabaseandmodel = Table(
    "researchdatabaseandmodel_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("researchdatabaseandmodel", pg.ARRAY(JSON)),
    schema="bronze",
)

researchmaterial = Table(
    "researchmaterial_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("researchmaterial", pg.ARRAY(JSON)),
    schema="bronze",
)

softwareandtechnicalproduct = Table(
    "softwareandtechnicalproduct_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("softwareandtechnicalproduct", pg.ARRAY(JSON)),
    schema="bronze",
)

spinout = Table(
    "spinout_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("spinout", pg.ARRAY(JSON)),
    schema="bronze",
)

publication = Table(
    "publication_raw",
    metadata,
    Column("links", pg.ARRAY(JSON)),
    Column("ext", JSON),
    Column("page", Integer),
    Column("size", Integer),
    Column("totalPages", Integer),
    Column("totalSize", Integer),
    Column("publication", pg.ARRAY(JSON)),
    schema="bronze",
)

tracker = Table(
    "tracker",
    metadata,
    Column("entity", String, primary_key=True),
    Column("page", Integer),
    Column("status", String),
    Column("timestamp", DateTime, default=func.current_timestamp()),
    schema="bronze",
)

api_page = Table(
    "api_page",
    metadata,
    Column("timestamp", DateTime, default=func.current_timestamp()),
    Column("entity", String, primary_key=True),
    Column("page", Integer, primary_key=True),
    Column("total_pages", Integer),
    Column("raw_data", pg.ARRAY(JSON)),
    schema="bronze",
)
