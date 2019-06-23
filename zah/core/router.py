"""This module is the base for creating, matching or rendering routes
for the application.
"""

class DefaultRouter:
    """This the base class to create and match routes for the application.
    The routes are created in `routes' dictionnary` that is persistent
    during the application's lifecycle.
    """
    def __init__(self):
        self.routes = {}

    def add_route(self, path, view, name, **context):
        """Add a route to the dictionnary of routes that will
        be used by the application:

            {
                name: {
                    path: /,
                    view: callable(),
                    context: {}
                }
            }
        """
        self.routes.update(
            {
                name: {
                    'path': path,
                    'view': self.check_view(view),
                    'context': context
                }
            }
        )

    def match_route(self, route):
        """Return a specific route as a dictionnary:

            {
                name: {
                    path: /,
                    view: callable(),
                    context: {}
                }
            }
        """
        if not isinstance(route, str):
            pass

        try:
            route = self.routes.get(route)
        except KeyError:
            raise
        return route

    @staticmethod
    def check_view(view):
        """Checks if the view is a callable that
        can return a function that returns some kind
        of html string
        """
        if callable(view):
            return view
        raise TypeError()

class RegexRouter(DefaultRouter):
    def add_route(self, regex_path, view, name, **context):
        """Add a REGEX route to the dictionnary of routes that will
        be used by the application:

            {
                name: {
                    path: ^$,
                    view: callable(),
                    context: {}
                }
            }
        """
        self.routes.update(
            {
                name: {
                    'path': regex_path,
                    'view': self.check_view(view),
                    'context': context
                }
            }
        )