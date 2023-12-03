from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from zah.conf import settings


class TemplateBackend:
    def __init__(self):
        self.environment = Environment(
            loader=FileSystemLoader(settings.TEMPLATES),
            autoescape=True
        )


template_backend = TemplateBackend()
