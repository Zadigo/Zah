import os

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_PATH, 'static')

TEMPLATES = os.path.join(BASE_PATH, 'templates')

TEMPLATE_BACKEND = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
