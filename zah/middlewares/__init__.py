import inspect
from importlib import import_module

from zah.conf import settings


class Middlewares:
    """Functions that are executed in the order
    in which they were registered and on the request"""

    MODULES = {}
    middlewares = {}

    def __init__(self):
        for middleware in settings.MIDDLEWARE:
            module_path, expected_name = middleware.rsplit('.', maxsplit=1)
            module = import_module(module_path)

            results = inspect.getmembers(module, inspect.isclass)
            for name, klass in results:
                if name == expected_name:
                    self.middlewares[name.lower()] = klass

            self.MODULES[module_path] = module

        self.app = None

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.middlewares}]>'

    def __getitem__(self, name):
        return self.middlewares[name]

    def prepare(self, app):
        self.app = app

    def run_middlewares(self, request, view_func, response):
        previous_response = None
        for middleware in self.middlewares.values():
            if previous_response is not None:
                instance = middleware(previous_response)
                previous_response = instance(request)
            else:
                instance = middleware(response)
                previous_response = instance(request)
        return response


class MiddlewareMixin:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        response = None
        response = self.request_processor(request)
        response = self.response_processor(request, response)
        return response

    def response_processor(self, request, response):
        return response

    def request_processor(self, request):
        return self.response

    def view_processor(self, request, response, view_func):
        return self.response
