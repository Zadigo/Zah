import datetime
import warnings
from datetime import datetime, timedelta
from typing import Any, Tuple, Union
from urllib.parse import quote, urlparse, urlunparse
from werkzeug.urls import iri_to_uri
from werkzeug.http import http_date
from werkzeug._internal import _to_str, _to_bytes, _make_cookie_domain, _cookie_quote

from werkzeug.wrappers import Response
# def convert_to_bytes(value: Union[str, bytes], charset: str = 'utf-8', errors: str = 'strict'):
#     if value is None or isinstance(value, bytes):
#         return value

#     if isinstance(value, str):
#         return value.encode(charset, errors)
#     else:
#         raise ValueError('Expected bytes')


# def convert_to_string(value: Any, charset: str = 'utf-8', errors: str = 'strict', allow_none_charset: bool = False):
#     if value is None or isinstance(value, str):
#         return value

#     if charset is None:
#         if allow_none_charset:
#             return value

#     return value.decode(charset, errors)


# def convert_iri_to_uri(iri: Union[str, Tuple], charset: str = 'utf-8', errors: str = 'strict', safe_conversion: bool = 'False'):
#     if isinstance(iri, tuple):
#         iri = urlunparse(iri)

#     if safe_conversion:
#         pass

#     iri = urlparse(convert_to_string(iri, charset=charset, errors=errors))
#     path = quote(iri.path, errors=errors)


class Cookie:
    # key, value, max_age, expires, path, domain, secure
    # http_only, charset, sync_expires, max_size, same_site
    def __init__(self, key: str, **kwargs):
        charset = kwargs.get('charset', 'utf-8')
        key = _to_bytes(key, charset=charset)
        value = _to_bytes(kwargs.get('value'), charset=charset)

        path = kwargs.get('path', None)
        if path is not None:
            path = iri_to_uri(path, charset)

        domain = _make_cookie_domain(kwargs.get('domain'))

        max_age = kwargs.get('max_age', None)
        if isinstance(max_age, timedelta):
            max_age = int(max_age.total_seconds())

        expires = kwargs.get('expires')
        if expires is not None:
            if not isinstance(expires, str):
                expires = http_date(expires)
        elif max_age is not None and kwargs.get('sync_expires', False):
            expires = http_date(datetime.now(tz=datetime.timezone.utc).timestamp() + max_age)

        same_site = kwargs.get('same_site', None)
        if same_site is not None:
            same_site = same_site.title()

            if same_site not in ['Strict', 'Lax', 'None']:
                raise ValueError('same site must be one of ')

        buffer = [key + b'=' + _cookie_quote(value)]

        cookie_attrs = [
            (b'Domain', domain, True),
            (b'Expires', expires, False),
            (b'Max-Age', max_age, False),
            (b'Secure', kwargs.get('secure', False), None),
            (b'HttpOnly', kwargs.get('http_only', False), None),
            (b'Path', path, False),
            (b'SameSite', same_site, False),
        ]

        for key, value, f in cookie_attrs:
            if f is None:
                if value:
                    buffer.append(key)
                continue

            if value is None:
                continue

            temp = bytearray(key)
            if not isinstance(value, (bytes, bytearray)):
                value = _to_bytes(str(value), charset)
            if f:
                value = _cookie_quote(value)
            temp += b'=' + value
            buffer.append(bytes(temp))

        return_value = b'; '.join(buffer)
        return_value = return_value.decode('latin1')
        
        cookie_size = len(return_value)

        max_size = kwargs.get('max_size', 4093)
        if max_size and cookie_size > max_size:
            value_size = len(value)
            warnings.warn(
                f"The {key.decode(charset)!r} cookie is too large: the value was"
                f" {value_size} bytes but the"
                f" header required {cookie_size - value_size} extra bytes. The final size"
                f" was {cookie_size} bytes but the limit is {max_size} bytes. Browsers may"
                f" silently ignore cookies larger than this.",
                stacklevel=2,
            )

        self.return_value = return_value

    def __call__(self, key: str, **kwargs):
        self.__init__(key, **kwargs)
        return self.return_value

    def get_cookie(self):
        return self.return_value

cookie = Cookie('some key')
print(cookie.get_cookie())
