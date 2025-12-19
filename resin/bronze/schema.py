"""
The bronze layer reflects the raw data from the GTR API.
"""

from sqlalchemy import JSON, Column, DateTime, Integer, String, Table
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.sql import func

from ..metadata import metadata

# Entity tables - each follows the structure from fetcher.py
fund_raw = Table(
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

project_raw = Table(
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

person_raw = Table(
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

organisation_raw = Table(
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

artisticandcreativeproduct_raw = Table(
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

collaboration_raw = Table(
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

dissemination_raw = Table(
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

futherfunding_raw = Table(
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

impactsummary_raw = Table(
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

intellectualproperty_raw = Table(
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

keyfinding_raw = Table(
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

policyinfluence_raw = Table(
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

product_raw = Table(
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

researchdatabaseandmodel_raw = Table(
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

researchmaterial_raw = Table(
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

softwareandtechnicalproduct_raw = Table(
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

spinout_raw = Table(
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

publication_raw = Table(
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

# Tracker table for managing fetch progress
tracker = Table(
    "tracker",
    metadata,
    Column("entity", String, primary_key=True),
    Column("page", Integer),
    Column("status", String),
    Column("timestamp", DateTime, default=func.current_timestamp()),
    schema="bronze",
)
