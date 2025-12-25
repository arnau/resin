"""
SQLAlchemy utilities for the resin package.
"""

from typing import Any, Type, Union

from sqlalchemy import BigInteger, func
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
    return func.cast(func.json_extract_string(column, path), type_)


def json_extract_timestamp(column: ColumnElement[Any], path: str):
    """Assumes data is in milliseconds"""
    return func.to_timestamp(
        func.cast(func.json_extract(column, path), BigInteger) / 1000
    )


def path_extract(column: ColumnElement[Any], index: int):
    """Extracts a path segment"""
    return func.array_extract(func.parse_path(column), index)


__all__ = [
    "CreateTableAs",
    "CreateTableIfNotExists",
    "json_extract_as",
    "print_sql",
    "SqlFormatter",
]
