import os
from .sqlite import SqliteRepository
from .base import RepositoryInterface
from typing import Optional


DATABASES = {
    "sqlite": SqliteRepository
}


def create_repository(DATABASE_META: dict) -> Optional[RepositoryInterface]:
    try:
        db = DATABASES[DATABASE_META["TYPE"]](DATABASE_META["URL"])
    except KeyError:
        return False
    if not db.test_connection():
        return False
    if not db.initialize():
        return False
    return db

