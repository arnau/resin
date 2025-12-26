# %% prelude
import json
from datetime import datetime

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
from resin.api_client import api_entities
from resin.database import get_engine
from resin.sqlalchemy import SqlFormatter, print_sql

engine = get_engine("test")

# %%
#


print_sql(silver.link.link_select())

# %%
print_sql(bronze.api_entity.insert(api_entities), {"formatter": SqlFormatter.Nil})
