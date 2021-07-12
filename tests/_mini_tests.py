from django.views.decorators.cache import cache_page
from collections import defaultdict
from django.utils.regex_helper import _lazy_re_compile
from werkzeug.wrappers import Response
from werkzeug.test import create_environ


cc_delim_re = _lazy_re_compile(r'\s*,\s*')

environ = create_environ('/home', 'http://127.0.0.1:5000')
response = Response(environ)
response.headers.set('Cache-Control', 'max-age=3600,public,must-revalidate')

@cache_page
def patch_cache_control(response, **kwargs):
    def dictitem(s):
        t = s.split('=', 1)
        if len(t) > 1:
            return (t[0].lower(), t[1])
        else:
            return (t[0].lower(), True)

    def dictvalue(*t):
        if t[1] is True:
            return t[0]
        else:
            return '%s=%s' % (t[0], t[1])

    cc = defaultdict(set)
    if response.headers.get('Cache-Control'):
        for field in cc_delim_re.split(response.headers.get('Cache-Control')):
            directive, value = dictitem(field)
            if directive == 'no-cache':
                # no-cache supports multiple field names.
                cc[directive].add(value)
            else:
                cc[directive] = value

    # If there's already a max-age header but we're being asked to set a new
    # max-age, use the minimum of the two ages. In practice this happens when
    # a decorator and a piece of middleware both operate on a given view.
    if 'max-age' in cc and 'max_age' in kwargs:
        kwargs['max_age'] = min(int(cc['max-age']), kwargs['max_age'])

    # Allow overriding private caching and vice versa
    if 'private' in cc and 'public' in kwargs:
        del cc['private']
    elif 'public' in cc and 'private' in kwargs:
        del cc['public']

    for (k, v) in kwargs.items():
        directive = k.replace('_', '-')
        if directive == 'no-cache':
            # no-cache supports multiple field names.
            cc[directive].add(v)
        else:
            cc[directive] = v

    directives = []
    for directive, values in cc.items():
        if isinstance(values, set):
            if True in values:
                # True takes precedence.
                values = {True}
            directives.extend([dictvalue(directive, value)
                               for value in values])
        else:
            directives.append(dictvalue(directive, values))
    cc = ', '.join(directives)
    response.headers.set('Cache-Control', cc)

patch_cache_control(response, max_age=1500)
