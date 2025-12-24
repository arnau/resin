"""
Database engine configuration for the resin package.
"""

import atexit

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.pool import StaticPool

# Global engine instance
_engine = None


def get_engine(suffix: str | None = None) -> Engine:
    """Get the configured DuckDB engine with attached databases."""
    global _engine

    if _engine is None:
        _engine = _create_engine(suffix)

    return _engine


def get_connection(suffix: str | None = None):
    """Get a raw database connection with attached databases."""
    engine = get_engine(suffix)
    return engine.raw_connection()


def _create_engine(suffix: str | None = None) -> Engine:
    """Create and configure the DuckDB engine."""
    engine = create_engine(
        "duckdb:///:memory:",
        poolclass=StaticPool,
    )

    # Determine database file names
    bronze_parts = [part for part in ["resin", suffix, "bronze"] if part is not None]
    silver_parts = [part for part in ["resin", suffix, "silver"] if part is not None]
    bronze_db = "_".join(bronze_parts) + ".duckdb"
    silver_db = "_".join(silver_parts) + ".duckdb"

    # Attach databases on first connection
    with engine.connect() as conn:
        conn.execute(
            text(f"""
            attach '{bronze_db}' as bronze;
            attach '{silver_db}' as silver;
        """)
        )
        conn.commit()

    return engine


def reset_engine():
    """Reset the engine (useful for testing)."""
    global _engine
    if _engine is not None:
        _engine.dispose()
    _engine = None


def cleanup():
    """Cleanup database connections and WAL files."""
    global _engine
    if _engine is not None:
        try:
            # Close all connections properly
            with _engine.connect() as conn:
                conn.execute(text("CHECKPOINT;"))
                conn.commit()
        except Exception:
            # Ignore errors during cleanup
            pass
        finally:
            _engine.dispose()
    _engine = None


# Register cleanup function to run at exit
atexit.register(cleanup)
