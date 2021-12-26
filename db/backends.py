import sqlite3
from functools import cached_property

from zah.settings import settings


class SQLiteBackend:
    def __init__(self):
        db_name = settings.DATABASE['name']
        self.conn = sqlite3.connect(f"{db_name}.sqlite", timeout=1000)

    @property
    def get_cursor(self):
        return self.conn.cursor()
