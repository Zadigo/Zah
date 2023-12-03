from zah.middlewares import Middlewares


class Registry:
    def __init__(self):
        self.app = None
        self.middlewares = Middlewares()

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.app}]>'

    def prepare(self, app):
        self.app = app
        self.middlewares.prepare(app)


registry = Registry()
