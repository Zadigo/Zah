import os
from importlib import import_module
from zah.models.base import Model

def get_project_path(path):
    return os.path.dirname(path)

def get_models(path):
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
                has_module = True
                break

    if has_module:
        try:
            # Import the module
            module = import_module('ZahWebsite.models')
        except ImportError:
            raise

        models = {}
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
        # Base path
        self.base_path = os.path.dirname(project_path)
        # Project name
        self.project_name = os.path.basename(self.base_path)
        # Templates path
        self.templates_path = os.path.join(self.base_path, 'templates')
        # Models' path
        self.app_models = get_models(self.base_path)