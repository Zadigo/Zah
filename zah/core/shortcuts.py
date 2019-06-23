from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from zah.core.router import DefaultRouter
from zah.core.settings import Configuration

# FIXME: The configuration dict is resinstanciated hence
# we are losing the project path and preventing jinja
# from loading the correct template
templates = Environment(loader=FileSystemLoader(Configuration().templates_path), autoescape=True)

# configuration = Configuration()

def render(request, template_name, context=None):
    """Shortcut for returning a view as an HTML output
    to a response for a request
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

# def redirect(to, permanent=False):
#     """Shortcut for redirecting to a route. `to` should
#     be a qualified named route
#     """
#     def view(**kwargs):
#         try:
#             # Get the route in the 
#             # routes' dictionnary
#             route = DefaultRouter.match_route(to)
#         except RouteError:
#             pass

#         # Return the viewfunction associated
#         # with the route
#         return route['view']
#     return view
