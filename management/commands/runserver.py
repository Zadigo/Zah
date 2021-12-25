import os
from importlib import import_module

from zah.admin.interface import admin_interface
from zah.apps import apps
from zah.management.base import ProjectCommand
from zah.settings import settings


class Command(ProjectCommand):
    def add_arguments(self, parser):
        # parser.add_arguments()
        pass
    
    def execute(self, namespace=None):
        project_settings_python_path = os.environ.get('ZAH_WEB_PROJECT')
        project_dotted_path = project_settings_python_path.rsplit('.', maxsplit=1)[0]
        configured_settings = settings(project=project_dotted_path)

        if self.requires_checks:
            pass
        
        # 1. Load all the default applications
        # required to run the project and set
        # them in the global Apps
        default_apps = configured_settings.APPS
        for app in default_apps:
            dotted_path, lookup_element = app.rsplit('.', maxsplit=1)
            try:
                app_module = import_module(dotted_path)
            except:
                raise ImportError('Could not import app')
            else:
                obj = getattr(app_module, lookup_element, None)
                if obj is None:
                    raise KeyError('Could not load element in app')
                apps.register(app_module, obj())
        configured_settings['DEFAULT_APPS'] = apps
        # print(apps.get_app_by_name('router'))
        
        # 2. If there is an urls file in the project, load it
        # so that the router can be configured if the project
        # does require/configure one
        router = apps.get_app_instance('router')
        try:
            urls_module = import_module(f"{project_dotted_path}.urls")
        except:
            pass
        else:
            patterns = getattr(urls_module, 'patterns')
            for pattern in patterns:
                router.add_route(**pattern)
                
        # 2. Load the default admin interface for the
        # whole project. This requires the router to
        # be configured so that we can integrate the
        # admin interface urls
        for pattern in admin_interface.urls:
            router.add_route(**pattern)

        # 3. If the project requires a database,
        # configure the global database
        
        # 4. Once we've loaded the side pieces,
        # load the main project entrypoint file app.py
        try:
            app_module = import_module(f"{project_dotted_path}.app")
        except:
            raise ImportError('The project does not have an app.py file')
        else:
            app_entrypoint_object = getattr(app_module, 'app', None)
            if app_entrypoint_object is None:
                    raise Exception("app.py does not have an 'app' attribute for starting the webserver")
            # This is where we start the webserver 
            app_entrypoint_object.create()
