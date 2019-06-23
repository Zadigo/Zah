import os
from importlib import import_module

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from zah.models.base import Model


def get_project_path(path):
    return os.path.dirname(path)

def get_models(path):
    has_models_module = False
    # Walk the folder
    root_path = list(os.walk(path))[0]
    for item in root_path:
        # Get the files at the root
        # of the application:
        # e.g. path, [a, b], [c, d])
        if isinstance(item, list):
            if 'models.py' in item:
                # The first models.py file we find,
                # we stop immediately
                has_models_module = True
                break

    # Dictionnary for all registered
    # models of the created application
    models = {}

    if has_models_module:
        try:
            # Import the module
            module = import_module('ZahWebsite.models')
        except ImportError:
            raise

        # Get module's objects
        module_dict = dict(module.__dict__)
        for key, value in module_dict.items():
            if key.startswith('__'):
                pass
            else:
                # Get the models
                if isinstance(value, type) and issubclass(value, Model) and key != 'Model':
                    # Update the models' dictionnary
                    models.update({key: value})
    return models

class Configuration:
    def __init__(self, project_path=None):
        # FIXME: The appllication breaks when a project
        # path is not provided because os.path requires
        # a valid path
        # HACK: Replace by local __file__ for now
        if project_path is None:
            project_path = __file__

        # Base path
        self.base_path = os.path.dirname(project_path)
        # Project name
        self.project_name = os.path.basename(self.base_path)
        # Templates path
        self.templates_path = os.path.join(self.base_path, 'templates')
        # Models' path
        self.app_models = get_models(self.base_path)
        # Secret key
        self.secret_key = None
        # Jinja environment
        self.jinja_environment = Environment(loader=FileSystemLoader(self.templates_path), autoescape=True)
        # Request headers
        self.headers = {}

    def populate_headers(self, **kwargs):
        """Creates the base headers that will be used
        in the different requests
        """
        headers = {
            'test': 'a'
        }
        return {**headers, **kwargs}

    def __repr__(self):
        return str(self.__dict__)
