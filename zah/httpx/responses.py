from werkzeug import exceptions
from werkzeug.wrappers import Response


class HttpResponse(Response):
    """Base HTTP response used to render templates
    strings for the application"""

    default_mimetype = 'text/html'
    status_code = 200
    description = None
    
    def __init__(self, template_string, headers=None):
        attrs = {
            'status': self.status_code,
            'headers': headers,
            'mimetype': self.default_mimetype
        }
        super().__init__(template_string, **attrs)


class HttpResponseBadRequest(HttpResponse):
    status_code = 400


class HttpResponseNotFound(HttpResponse):
    pass


class HttpResponseForbidden(HttpResponse):
    status_code = 405


class HTTPMethodNotAllowed(exceptions.MethodNotAllowed):
    status_code = 406


class HttpResponseGone(HttpResponse):
    pass


class HttpResponseServerError(HttpResponse):
    status_code = 500


class Http404(exceptions.NotFound):
    status_code = 404
    description = "The page you are looking for does not exist"


class JsonResponse(HttpResponse):
    default_mimetype = 'application/json'

    def __init__(self, data, headers={}):
        super().__init__(data, headers)
