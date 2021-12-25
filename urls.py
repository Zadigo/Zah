import os
from functools import partial
from typing import Callable, Union

from werkzeug.wrappers import Request

# from zah import get_template_backend
from zah.responses import HttpResponse
from zah.router.shortcuts import get_router
from zah.settings import settings

TEMPLATE_BACKEND = settings.TEMPLATE_BACKEND

def render_page(template: str, context: dict = {}):
    """Renders an HTML page within the add_route function"""
    def view(**kwargs):
        base_context = context | kwargs.get('context', {})
        template_obj = TEMPLATE_BACKEND.get_template(template)
        # return kwargs.get('request'), template_obj.generate(base_context)
        return HttpResponse(template_obj.generate(base_context))
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
