"""
Bronze layer initialization command.
"""

from collections.abc import Generator

from resin.bronze import create_tables
from resin.database.engine import get_engine


def main(db: str | None = None) -> Generator[str, None, None]:
    """Create bronze layer tables."""
    engine = get_engine(db)
    with engine.connect() as conn:
        create_tables(conn)
        conn.commit()
    yield "Bronze tables created."
