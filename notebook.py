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
from resin.database import get_engine
from resin.sqlalchemy import SqlFormatter, print_sql

engine = get_engine("test")

# %% silver.organisation_address
# TODO
data = {"page": 1, "totalPages": 10, "person": [{"id": 1, "name": "John Doe"}]}
print_sql(bronze.api_page.entity_insert2("person", json.dumps(data, indent=None)))
