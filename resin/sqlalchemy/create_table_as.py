"""
CreateTableAs implementation for SQLAlchemy.
"""

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.expression import Executable


class CreateTableAs(Executable, ClauseElement):
    inherit_cache = False

    def __init__(self, name, query):
        self.name = name
        self.query = query


@compiles(CreateTableAs)
def visit_create_table_as(element, compiler, **kw):
    return "CREATE TABLE %s AS %s" % (
        element.name,
        compiler.process(element.query, **kw),
    )
