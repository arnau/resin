"""
Silver layer initialisation command.
"""

from collections.abc import Generator

from resin.database.engine import get_engine
from resin.silver import create_tables


def main(db: str | None = None) -> Generator[str, None, None]:
    """Create silver layer tables."""
    engine = get_engine(db)
    with engine.connect() as conn:
        create_tables(conn)
        conn.commit()
    yield "Silver tables created."
