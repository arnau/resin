"""
Singleton metadata instance for the resin package.
"""

from sqlalchemy import MetaData

# Singleton metadata instance to be shared across all table definitions
metadata = MetaData()
