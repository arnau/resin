"""
Database engine configuration for the resin package.
"""

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.pool import StaticPool

# Global engine instance
_engine = None


def get_engine() -> Engine:
    """Get the configured DuckDB engine with attached databases."""
    global _engine

    if _engine is None:
        _engine = _create_engine()

    return _engine


def get_connection():
    """Get a raw database connection with attached databases."""
    engine = get_engine()
    return engine.raw_connection()


def _create_engine() -> Engine:
    """Create and configure the DuckDB engine."""
    engine = create_engine(
        "duckdb:///:memory:",
        poolclass=StaticPool,
    )

    # Attach databases on first connection
    with engine.connect() as conn:
        conn.execute(
            text("""
            attach 'resin_bronze.duckdb' as bronze (READ_ONLY);
            attach 'resin_silver.duckdb' as silver;
            use silver;
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
