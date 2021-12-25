import os

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import pathlib


# The base path for your project for more information
# please consult http://example.com

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# The default location of the static folder
# for your application

STATIC_ROOT = os.path.join(BASE_PATH, 'static')

MEDIA_ROOT = os.path.join(BASE_PATH, 'media')

# The default location of the templates
# folder for your application

TEMPLATES = os.path.join(BASE_PATH, 'templates')

# This is the default template backend where
# Zah searches and serves the different the
# html files

TEMPLATE_BACKEND = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)

TEMPLATE_ENGINE = {
    'root': os.path.join(BASE_PATH, 'templates'),
    'backend': Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
}

# Use this to indicate where the frontend
# app is located so that Jinja can serve
# the index.html file of the VueJS
# application

FRONT_END_ROOT = None
