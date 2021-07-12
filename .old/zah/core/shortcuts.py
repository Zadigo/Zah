from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from zah.core.settings import Configuration

templates = Environment(loader=FileSystemLoader(Configuration().templates_path), autoescape=True)

def render(request, template_name, context=None):
    """Shortcut for returning a view object
    """
    # Protect the render function against
    # TypeError() because Jinja expects a dict
    # to iterate upon for the template
    if context is None:
        context = {}

    def view(**kwargs):
        # Pass the template name
        template = templates.get_template(template_name)
        if kwargs:
            context.update(kwargs)
        # Output the HTML string back
        # to a given response
        return template.render(context)
    return view
