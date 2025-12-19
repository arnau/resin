"""
CreateTableAs implementation for SQLAlchemy.
"""

from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.compiler import DDLCompiler
from sqlalchemy.sql.expression import Executable


class CreateTableAs(Executable, ClauseElement):
    inherit_cache = False

    def __init__(self, name: str, query: ClauseElement) -> None:
        self.name = name
        self.query = query


@compiles(CreateTableAs)
def visit_create_table_as(
    element: CreateTableAs, compiler: DDLCompiler, **kw: Any
) -> str:
    return "CREATE TABLE %s AS %s" % (
        element.name,
        compiler.process(element.query, **kw),  # type: ignore
    )
