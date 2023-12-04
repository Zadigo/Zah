from zah.middlewares import Middlewares


class MasterRegistry:
    def __init__(self):
        self.app = None
        self.is_ready = False
        self.project_name = None
        self.absolute_path = None
        self.middlewares = Middlewares()

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.app}]>'

    def pre_configure_project(self):
        pass

    def populate(self, app):
        from zah.conf import settings
        self.app = app
        self.pre_configure_project()
        self.middlewares.prepare(app)
        settings['registry'] = self
        self.is_ready = True


registry = MasterRegistry()
