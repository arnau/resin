# %% prelude
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
    literal,
    literal_column,
    select,
    text,
)
from sqlalchemy.dialects import postgresql as pg

from resin import bronze, metadata, silver
from resin.database import get_engine
from resin.sqlalchemy import SqlFormatter, print_sql

engine = get_engine(test=True)

# %% silver.organisation_address
# TODO
print_sql(silver.org_mod.organisation_raw())
