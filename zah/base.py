import datetime
import os
from importlib import import_module

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from werkzeug.wrappers import Request, Response

from zah.core import router
from zah.core.settings import Configuration
from zah.errors import routes


class Zah:
    def __init__(self, file_path):
        # Base path
        self.base_path = os.path.dirname(os.path.abspath(file_path))
        # Templates path
        self.templates_path = os.path.join(self.base_path, 'zah/templates')
        # Router class
        self.router = router.DefaultRouter()
        # Jinja environment
        # self.templates = Environment(loader=FileSystemLoader(self.templates_path), autoescape=True)
        # Base headers for the request
        self.headers = {}

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

    # def register_models(self, model):
    #     """Register a list of models to be used with
    #     the application. Model should be a module path
    #     such as `x.models`
    #     """
    #     registered_models = []
    #     if isinstance(model, str):
    #         try:
    #             # Import the models module
    #             models = import_module('zah.models')
    #         except ImportError:
    #             raise
    #         for name, model in models.items():
    #             if callable(model) and issubclass(model, ''):
    #                 registered_models.append(model)
    #     else:
    #         pass
        
    #     return registered_models
