"""
SQLAlchemy utilities for the resin package.
"""

from typing import Any, Type, Union

from sqlalchemy import JSON as Json
from sqlalchemy import UUID as Uuid
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Insert,
    Integer,
    String,
    Table,
    literal_column,
    select,
)
from sqlalchemy import func as fn
from sqlalchemy.dialects.postgresql import ARRAY as Array
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.type_api import TypeEngine

from .create_table_as import CreateTableAs
from .create_table_if_not_exists import CreateTableIfNotExists
from .printer import SqlFormatter, print_sql


def json_extract_as(
    column: ColumnElement[Any],
    path: str,
    type_: Union[Type[TypeEngine[Any]], TypeEngine[Any]],
):
    return fn.cast(fn.json_extract_string(column, path), type_)


def json_extract_timestamp(column: ColumnElement[Any], path: str):
    """Assumes data is in milliseconds"""
    return fn.to_timestamp(fn.cast(fn.json_extract(column, path), BigInteger) / 1000)


def list_trim(list_: ColumnElement[Any]):
    return fn.list_transform(list_, literal_column("lambda x : trim(x)"))


# Function aliases
pick = fn.json_extract_string
pick_as = json_extract_as
pick_as_ts = json_extract_timestamp
unnest = fn.unnest


def path_extract(column: ColumnElement[Any], index: int):
    """Extracts a path segment"""
    return fn.array_extract(fn.parse_path(column), index)


JsonArray = Array(Json)

__all__ = [
    "CreateTableAs",
    "CreateTableIfNotExists",
    # Functions
    "json_extract_as",
    "pick",
    "pick_as",
    "pick_as_ts",
    "unnest",
    "list_trim",
    # Debugging helpers
    "print_sql",
    "SqlFormatter",
    # sqlalchemy re-exports
    "select",
    "insert",
    "fn",
    # types
    "BigInteger",
    "Integer",
    "String",
    "Boolean",
    "Uuid",
    "Json",
    "Array",
    "JsonArray",
    "DateTime",
    "Insert",
    "ColumnElement",
    "Column",
    "Table",
]
