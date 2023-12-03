import pathlib


DEBUG = True


ZAH_PROJECT_PATH = pathlib.Path(__file__).parent.parent.absolute()


# The base path to your project
# see:
PROJECT_PATH = pathlib.Path(__file__).parent.parent.absolute()


# Apps to load in addition for
# the current project
APPS = [
    'zah.router.app.Router'
]


# The default location of the static folder
# for your application
STATIC_ROOT = PROJECT_PATH / 'static'


# The default location of the templates
# folder for your application
TEMPLATES = [
    PROJECT_PATH / 'templates'
]


# TEMPLATES = {
#     'directories': []
# }


MIDDLEWARE = [
    'zah.middlewares.debug.Debug'
]


# Use this to indicate where the frontend
# app is located so that Jinja can serve
# the index.html file of the VueJS
# application


FRONT_END_ROOT = None


DATABASE = {
    'backend': 'sqlite',
    'name': '',
}
