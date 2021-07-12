from werkzeug import exceptions
from werkzeug.wrappers import Response

class HTTP404(exceptions.NotFound):
    description = "The page you are looking for does not exist"


class HTTPMethodNotAllowed(exceptions.MethodNotAllowed):
    pass


class HttpResponse(Response):
    def __init__(self, template_string, status=None, headers=None, mimetype='text/html'):
        super().__init__(template_string, status=status, headers=headers, mimetype=mimetype)
