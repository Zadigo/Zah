from jinja2.environment import Environment

def get_template_backend():
    from zah.settings import settings
    backend = getattr(settings, 'TEMPLATE_BACKEND', None)
    if not isinstance(backend, Environment):
        raise ValueError('Backend should be an instance of Jinja template backend')
    return backend
from django.shortcuts import redirect
