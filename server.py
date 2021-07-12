from collections import OrderedDict
from typing import Callable

import werkzeug
from werkzeug import exceptions
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request, Response

from zah import get_template_backend
from zah.context import RequestContext
from zah.responses import HTTP404, HttpResponse
from zah.router import Router
from zah.store import Store


class Descriptor:
    apps = OrderedDict()

    def __contains__(self, name):
        return name in self.apps

    def __getitem__(self, name):
        return self.apps[name]

    @property
    def has_store(self):
        instance = self.apps.get('store', None)
        if instance is None:
            return False
        return isinstance(instance, Store)

    @property
    def has_router(self):
        instance = self.apps.get('router', None)
        if instance is None:
            return False
        return isinstance(instance, Router)

    def new_app(self, app: type):
        name = app.__name__.lower()
        instance = app()
        self.apps.setdefault(name, instance)

    def has_app(self, name):
        return name in self.apps


class BaseServer:
    _routes = []
    has_router = False

    app_descriptor = Descriptor()

    headers = {
        'Content-Type': 'text/html; charset=utf8'
    }

    @classmethod
    def create(cls, host='127.0.0.1', port=5000, debug=True, **kwargs):
        attrs = {'use_reloader': True, 'use_debugger': True} | kwargs
        instance = cls()
        app_to_run = instance.app
        # if debug:
        #     app_to_run = SharedDataMiddleware(app_to_run, {'/static': None})
        werkzeug.run_simple(host, port, app_to_run, **attrs)

    def _dispatch_request(self, request: Request):
        attrs = {'mimetype': 'text/html', 'headers': self.headers}
        template_to_render = get_template_backend().get_template('home.html')

        context = RequestContext(request)
        # Before processing the request,
        # match a given path for the
        # corresponding template
        if self.app_descriptor.has_router:
            router = self.app_descriptor.apps.get('router')

            candidate, candidates = router.match(request.path)
            if not candidate:
                return HTTP404(response=None)

            view = candidate['view']
            # We receive tuple (request, template (str)) and the
            # reason for that is to allow the decorators to
            # eventually modify or analyze the requests.
            # _, template_to_render = view(request=request, context=context)
            http_response = view(request=request, context=context)
            if isinstance(http_response, exceptions.HTTPException):
                return http_response
            return http_response
        return HttpResponse(template_to_render.render(context))

    def _build_request(self, environ, start_response):
        request = Request(environ)
        response = self._dispatch_request(request)
        return response(environ, start_response)

    def app(self, environ, start_response):
        """Entrypoint for starting the webserver"""
        return self._build_request(environ, start_response)

    def use_component(self, component: type):
        if not isinstance(component, type):
            raise TypeError('Component should be a type')
        self.app_descriptor.new_app(component)

    def add_route(self, path: str, view: Callable, name=None):
        if not self.app_descriptor.has_router:
            raise ValueError('You need to implement a router before you can implement routes')
        router = self.app_descriptor.apps.get('router')
        router.add_route(path, view, name)
        self._routes = router.urls

    def as_route(self, path: str, name: str = None):
        """A decorator that transforms a function into a route"""
        def view(func):
            self.add_route(path, func, name)
        return view


# server = BaseServer()
# server.use_component(Router)
# server.add_route('/', render('home.html'), name='home')
# print(server._routes)
# server.use_component(Store)
# server.create()
