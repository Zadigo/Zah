import os

# The base path for your project for more information
# please consult http://example.com

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# The default location of the static folder
# for your application

STATIC_ROOT = os.path.join(BASE_PATH, 'static')

MEDIA_ROOT = os.path.join(BASE_PATH, 'media')

# The default location of the templates
# folder for your application

TEMPLATES = [
    # TODO: Cannot get the templates from within the
    # project because the correct base path does not
    # get integrated in the Jinja environment on
    # startup
    os.path.join(BASE_PATH, 'templates'),
    'D:/coding/personnal/zah/tests/project/templates'
]


# Use this to indicate where the frontend
# app is located so that Jinja can serve
# the index.html file of the VueJS
# application

FRONT_END_ROOT = None
