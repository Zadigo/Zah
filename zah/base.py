import datetime
import os
from importlib import import_module

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from werkzeug.wrappers import Request, Response

from zah.core import router
from zah.core.settings import Configuration
from zah.errors import routes

from zah.models.base import Model


class Zah:
    """
    `project_path` is the "_file_" magic string that will be used
    to guess certain elements of your application
    """
    def __init__(self, project_path):
        # Router class
        self.router = router.DefaultRouter()
        # Base headers for the request
        self.headers = {}
        # Configure settings
        self.configuration = Configuration(project_path=project_path)

    def dispatch(self, request):
        """Dispatch a request by returning a response.
        The response is a function: response(environ, start_application)
        """
        # template = GenericView().view(request, 'base.htm')
        # template = self.router._routes('home')
        # s = template['view']().view(request, 'base.htm')

        # The user asks for a route e.g. /
        route = 'home'
        # Search for the route in the registered routes
        matched_route = self.router.match_route(route)
        # Get the view function of the route in
        # order to render the template
        view_function = matched_route['view']
        # Execute the view function
        # and get the template as a string
        html_string = view_function(request)()
        # Render template in response
        response = Response(html_string, 200, self.headers, 'text/html')
        return response

    def wsgi_app(self, environ, start_application):
        # run_simple() takes the function by requiring
        # environ and start_application
        request = Request(environ)
        # Receive a response object
        response = self.dispatch(request)
        return response(environ, start_application)

    def register_models(self, models=[]):
        """Register a list of additional models to be used with
        the application. Model should be a module in a directory
        such as `x.models`
        """
        pass
