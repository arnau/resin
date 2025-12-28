# %% prelude
from datetime import datetime

from resin import bronze, silver
from resin.api_client import api_entities
from resin.database import get_engine
from resin.sql import SqlFormatter, print_sql

engine = get_engine("test")

# %%
# TODO: check links lookup for orcid_id. they should be filtered out. maybe others as well


print_sql(silver.publication.select_all())
