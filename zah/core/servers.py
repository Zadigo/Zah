from collections import OrderedDict

import werkzeug
from werkzeug import exceptions
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request
from werkzeug.wsgi import get_current_url, get_host, get_path_info

from zah.conf import settings
from zah.httpx.responses import Http404, HttpResponse
from zah.registry import registry
from zah.router import Router
from zah.template import template_backend
from zah.template.context import RequestContext


class ApplicationOptions:
    """Represents all the options and applications/
    components that are available within the project"""

    apps = OrderedDict()

    def __repr__(self):
        result = ', '.join(self.apps.keys())
        return f'<{self.__class__.__name__} [{result}]>'

    def __contains__(self, name):
        return name in self.apps

    def __getitem__(self, name):
        return self.apps[name]

    @property
    def has_store(self):
        from zah.store import Store

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

    def new_component(self, component):
        """Adds a new application or component
        to the options"""
        name = component.__name__.lower()
        verbose_name = name or component.verbose_name
        component_instance = component()
        self.apps.setdefault(name, component_instance)

    def has_app(self, name):
        return name in self.apps


class RouteMixin:
    """Adds functionnalities for adding routes
    for the current application

    >>> app = BaseServer()
    ...
    ... def my_view(request):
    ...     pass
    ...
    ... app.add_route('/', my_view, name='my_view')
    ... app.create()
    """
    routes = []
    has_router = False

    def add_route(self, path, view, name=None):
        """Add a route to the current application

        >>> app = BaseServer()
        ...
        ... def my_view():
        ...     pass
        ...
        ... app.add_route('/', my_view)
        """
        # path: str, view: Callable
        if path is None:
            raise ValueError('Path cannot be None')

        if not self.app_options.has_router:
            raise ValueError("You need to implement a router before "
                             "you can implement routes")

        router = self.app_options.apps.get('router')
        router.add_route(path, view, name)
        self.routes = router.urls

    def as_route(self, path, name=None):
        """A decorator that transforms a function into 
        a usable route

        >>> app = BaseServer()
        ...
        ... @app.as_route('/')
        ... def my_view():
        ...     pass
        """
        def view(func):
            self.add_route(path, func, name)
        return view


class BaseServer(RouteMixin):
    """Entrypoint for starting a server"""

    is_running = False
    app_options = ApplicationOptions()
    headers = {'Content-Type': 'text/html; charset=utf8'}

    def __call__(self, **kwargs):
        if not self.is_running:
            self.create(**kwargs)

    @classmethod
    def create(cls, host='127.0.0.1', port=5000, **kwargs):
        """Entrypoint for starting the webserver

        >>> app = BaseServer()
        ... app.create()
        """
        attrs = {'use_reloader': True, 'use_debugger': True} | kwargs
        instance = cls()
        instance.is_running = True
        registry.prepare(instance)
        werkzeug.run_simple(host, port, instance.app, **attrs)

    def _dispatch_request(self, request):
        """Dispatches the incoming request for a
        valid HttpResponse object"""

        # Populate the context with all
        # the necessary elements (apps...)
        # before passing it to the template
        context = RequestContext(request)
        context.populate(apps=self.app_options)

        if self.app_options.has_router:
            router = self.app_options.apps.get('router')

            candidate, candidates = router.match(request.path)
            if not candidate:
                return Http404(response=None)

            view = candidate['view']
            http_response = view(request)(context=context)
            registry.middlewares.run_middlewares(request, view, http_response)

            if isinstance(http_response, exceptions.HTTPException):
                return http_response
            return http_response

        attrs = {'mimetype': 'text/html', 'headers': self.headers}
        template_to_render = template_backend.environment.get_template(
            'index.html'
        )
        return HttpResponse(template_to_render.render(context))

    def _build_request(self, environ, start_response):
        """Constructs a Request to be disaptched in return
        for a valid HTTPResponse object"""
        request = Request(environ)
        response = self._dispatch_request(request)
        return response(environ, start_response)

    def app(self, environ, start_response):
        """Callable used to start the webserver and
        continuously run the app in `werkzeug.run_simple`"""
        registry.prepare(self)
        return self._build_request(environ, start_response)

    def use_component(self, component):
        """Add a callable to the current appliation
        to be used with the application"""
        if not isinstance(component, type):
            raise ValueError('Component should a callable')
        self.app_options.new_component(component)


class DevelopmentServer(BaseServer):
    """Base server to open a development server"""

    @classmethod
    def create(cls, host='127.0.0.1', port=5000, **kwargs):
        attrs = {'use_reloader': True, 'use_debugger': True} | kwargs
        new_instance = SharedDataMiddleware(
            cls.app,
            {'/static': str(settings.STATIC_ROOT)}
        )
        werkzeug.run_simple(host, port, new_instance, **attrs)
