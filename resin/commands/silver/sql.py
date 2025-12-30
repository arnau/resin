"""
Silver layer SQL command.
"""

from collections.abc import Generator

from resin import silver
from resin.sql import SqlFormatter, format_sql


def main(entity: str) -> Generator[str, None, None]:
    """Print the SQL for a silver entity's select_all() query."""
    if entity not in silver.__all__:
        yield f"Unknown entity: {entity}"
        return

    module = getattr(silver, entity)

    if not hasattr(module, "select_all"):
        yield f"Entity {entity} has no select_all function"
        return

    stmt = module.select_all()
    yield format_sql(stmt, {"formatter": SqlFormatter.SqlFmt})
