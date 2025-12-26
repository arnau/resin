"""
CreateTableIfNotExists DDL construct for SQLAlchemy.
"""

from typing import Any

from sqlalchemy import Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.compiler import DDLCompiler


class CreateTableIfNotExists(CreateTable):
    """A CreateTable variant that adds IF NOT EXISTS clause."""

    def __init__(self, element: "Table", **kw: Any) -> None:
        super().__init__(element, **kw)


@compiles(CreateTableIfNotExists)
def visit_create_table_if_not_exists(
    element: CreateTable, compiler: DDLCompiler, **kw: Any
) -> str:
    """Compile CreateTableIfNotExists to include IF NOT EXISTS clause."""
    text: str = compiler.visit_create_table(element, **kw)  # type: ignore
    text = text.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)
    return text
