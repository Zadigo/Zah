from werkzeug import exceptions
from werkzeug.wrappers import Response


class HttpResponse(Response):
    status_code = 200
    
    def __init__(self, template_string, headers=None, mimetype='text/html'):
        attrs = {
            'status': self.status_code,
            'headers': headers,
            'mimetype': mimetype
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
    description = "The page you are looking for does not exist"


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super().__init__(data, mimetype='application/json')


class HttpResponseRedirect(HttpResponse):
    status_code = 000
