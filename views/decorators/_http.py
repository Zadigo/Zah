from zah.responses import HTTPMethodNotAllowed

AUTHORIZED_METHODS = ['post', 'get']


def only_http_methods(*methods):
    methods = list(methods)

    def wrapper(func):
        def view(**kwargs):
            request = kwargs.get('request')
            authorized = [method.upper() for method in methods]
            if request.method not in authorized:
                return request, HTTPMethodNotAllowed()
            return func(**kwargs)
        return view
    return wrapper


only_GET = only_http_methods('get')
only_POST = only_http_methods('post')
only_SAFE = only_http_methods('get', 'head')
