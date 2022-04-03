def get_database_backend():
    # TEST
    from zah.db.backends import SQLiteBackend
    backend = SQLiteBackend()
    return backend
