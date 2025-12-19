"""
CreateTableIfNotExists DDL construct for SQLAlchemy.
"""

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.schema import Table


class CreateTableIfNotExists(CreateTable):
    """A CreateTable variant that adds IF NOT EXISTS clause."""

    def __init__(self, element, **kw):
        super().__init__(element, **kw)


@compiles(CreateTableIfNotExists)
def visit_create_table_if_not_exists(element, compiler, **kw):
    """Compile CreateTableIfNotExists to include IF NOT EXISTS clause."""
    text = compiler.visit_create_table(element, **kw)
    text = text.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)
    return text
