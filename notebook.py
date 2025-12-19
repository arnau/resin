# %% prelude
import duckdb
import sqlparse
from sqlalchemy import (
    JSON,
    UUID,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    literal_column,
    text,
)

from resin import bronze, silver
from resin.sqlalchemy import SqlFormatter, print_sql

conn = duckdb.connect(":memory:")
conn.execute("""
    attach 'resin_landing.duckdb' as landing (READ_ONLY);
    attach 'resin_omega.duckdb' as omega;
    use omega;
""")
metadata = MetaData()


# %% silver.organisation_address
