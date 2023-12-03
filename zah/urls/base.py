import os
import pathlib
from functools import partial, wraps
from typing import Callable, Union

from werkzeug.wrappers import Request

from zah.conf import settings
# from zah import get_template_backend
from zah.httpx.responses import HttpResponse
from zah.router.shortcuts import get_router
from zah.template import template_backend


def render_page(template, context={}):
    """Renders an HTML page based on a given route

    >>> def my_view():
    ...     return render_page('index.html')
    """
    def view(**kwargs):
        base_context = context | kwargs.get('context', {})
        template_to_render = template_backend.environment.get_template(
            template
        )
        return HttpResponse(template_to_render.generate(**base_context))

        # base_context = context | kwargs.get('context', {})
        # template_obj = template_backend.environment.get_template(template)
        # # template_obj = TEMPLATE_BACKEND.get_template(template)
        # # return kwargs.get('request'), template_obj.generate(base_context)
        # return HttpResponse(template_obj.generate(base_context))
    return view


def render(request: Request, template: str, context: dict = {}):
    """Returns an HTML page within a view function"""
    def view(**kwargs):
        base_context = context | kwargs.get('context', {})
        template_obj = TEMPLATE_BACKEND.get_template(template)
        # return kwargs.get('request'), template_obj.generate(base_context)
        return HttpResponse(template_obj.generate(base_context))
    return view(request=request)


def url(path: str, view: Callable, name: str = None, namespace: str = None):
    if path.startswith('/'):
        path = path.removeprefix('/')

    if not callable(view):
        raise TypeError('View should be a callable')
    config = {
        'path': path,
        'name': name.lower() if name is not None else name,
        'view': view
    }
    if namespace is not None:
        return {namespace: config}
    return config


def redirect(path: str, name: str):
    pass


def static(root: str, path: str):
    # from web import server_configuration
    static_project_path = os.path.join(root, 'static')
    return {path: static_project_path}
