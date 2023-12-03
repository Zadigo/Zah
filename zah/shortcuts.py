from zah.conf import settings
from zah.core.servers import BaseServer, DevelopmentServer


def get_default_server():
    """Return the default server for this project"""
    server = BaseServer
    if settings.DEBUG:
        server = DevelopmentServer
    return server()
