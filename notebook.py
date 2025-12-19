# %% prelude
import sqlalchemy
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
    text,
)

from resin import bronze, metadata, silver
from resin.database import get_engine
from resin.sqlalchemy import SqlFormatter, print_sql

engine = get_engine(test=True)
# conn = get_connection(test=True)
# %% create silver
with engine.connect() as conn:
    silver.create_tables(conn)

# %% silver
with engine.connect() as conn:
    result = conn.execute(text("DESCRIBE silver.person"))
    print(f"Silver person: {result.fetchone()}")


# %% silver.organisation_address
