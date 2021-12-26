import os

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

DEBUG = True

# The base path for your project

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

#

APPS = [
    'zah.router.app.Router'
]

# The default location of the static folder
# for your application

STATIC_ROOT = os.path.join(BASE_PATH, 'static')

# The default location of the templates
# folder for your application

TEMPLATES = [
    'D:/coding/personnal/zah/admin/templates'
]

# This is the default template backend where
# Zah searches and serves the different
# templates

_TEMPLATES = {
    'directories': []
}

TEMPLATE_BACKEND = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
# TEMPLATE_BACKEND.list_templates()

# Use this to indicate where the frontend
# app is located so that Jinja can serve
# the index.html file of the VueJS
# application

FRONT_END_ROOT = None

DATABASE = {
    'backend': 'sqlite',
    'name': '',
}
