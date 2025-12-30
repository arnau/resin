"""
Silver layer load command.
"""

from collections.abc import Generator

from resin import silver
from resin.database.engine import get_engine
from resin.silver import create_tables

MODULES = [name for name in silver.__all__ if name not in ("schema", "create_tables")]


def main(db: str | None = None) -> Generator[str, None, None]:
    """Load data into all silver tables."""
    engine = get_engine(db)

    with engine.connect() as conn:
        create_tables(conn)

        total = len(MODULES)
        for i, module_name in enumerate(MODULES, 1):
            module = getattr(silver, module_name)

            if not hasattr(module, "insert_all"):
                yield f"Skipping {module_name}: no insert_all function"
                continue

            stmt = module.insert_all()
            yield f"Loading {module_name} ({i}/{total})"
            conn.execute(stmt)

        conn.commit()

    yield "Silver load complete."
