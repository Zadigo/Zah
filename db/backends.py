import sqlite3
from functools import cached_property
from typing import Any

from zah.settings import settings


class SQLMixin:
    SELECT = 'SELECT {} from {} {}'
    
    @staticmethod
    def join(items):
        return ', '.join(items)
    
    def interprete_tokens(self, method, tokens: list, value: Any):
        columns = []
        retrieving_methods = ['filter', 'get']
        if method in retrieving_methods:
            for token in tokens:
                lh, rh = token
                columns.append(lh)
            c = self.join(columns)
                


class SQLiteBackend(SQLMixin):
    def __init__(self):
        db_name = settings.DATABASE['name']
        self.conn = sqlite3.connect(f"{db_name}.sqlite", timeout=1000)

    @property
    def get_cursor(self):
        return self.conn.cursor()
