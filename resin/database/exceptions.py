"""
Database exceptions.
"""


class DatabaseLockError(Exception):
    """Raised when a database file is locked by another process."""

    pass
