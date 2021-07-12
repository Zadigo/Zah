import re
import time

from collections import defaultdict
from zah.utils.dates import formatters

regex_compiler = re.compile(r'\s*,\s*')


def patch_cache_control(response, **kwargs):
    """
    A helper function to safelu modify and/or
    implement caching headers on a response

    Args:
        response ([type]): [description]
    """
    def directive_splitter(value):
        result = value.split('=', 1)
        if len(result) > 1:
            return (result[0].lower(), result[1])
        return (result[0], True)

    def directive_builder(directive, value):
        if value is True:
            return directive
        return f'{directive}={value}'

    current_cache_control = response.headers.get('Cache-Control', None)
    new_cache_headers = defaultdict(set)
    
    if current_cache_control is not None:
        for value in regex_compiler.split(current_cache_control):
            directive, value = directive_splitter(value)
            new_cache_headers[directive] = value

    # If new directives were passed in kwargs
    # implement them in the newly created headers
    # replacing them if necessary
    for key, new_value in kwargs.items():
        directive = key.replace('_', '-')
        new_cache_headers[directive] = new_value

    constructed_directives = []
    for directive, attrs in new_cache_headers.items():
        constructed_directives.append(
            directive_builder(directive, attrs)
        )
    final_header = ', '.join(constructed_directives)
    response.headers.set('Cache-Control', final_header)


def add_caching_directives(response, cache_timeout: int = None):
    """
    Implemnts `Expires` and `Cache-Control: max-age` on the
    response header

    Parameters
    ----------

        - response (Response): an HttpResponse or Response object
        - cache_timeout (int, optional): the cache timeout in seconds. Defaults to None.
    """
    if cache_timeout is None:
        cache_timeout = 1

    if cache_timeout < 0:
        cache_timeout = 0

    expire_header = response.headers.get('Expires', None)
    if expire_header is None:
        response.headers['Expires'] = formatters.formatdate(time.time() + cache_timeout)

    patch_cache_control(response, max_age=cache_timeout)


def cache_control(**attrs):
    def view_wrapper(func):
        def view(request, **kwargs):
            response = func(request=request, **kwargs)
            patch_cache_control(response, **attrs)
            return response
        return view
    return view_wrapper


def cache_page(func):
    pass


def never_cache(func):
    """
    Indicates the page should never be cached

    Parameters
    ----------

        func (Callable): a view function

    Returns
    -------

        view: a new view function with a response
              with patched cache control headers
    """
    def view(request, **kwargs):
        response = func(request=request, **kwargs)
        add_caching_directives(response, cache_timeout=-1)
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, private=True)
        return response
    return view
