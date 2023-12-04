import unittest
from typing import Deque
from werkzeug.test import create_environ
from werkzeug.wrappers import Request
from werkzeug.serving import WSGIRequestHandler
from zah.core.servers import BaseServer
# from zah.decorators import only_GET
from zah.router import Router
from zah.urls.base import render_page

# 1. Create a fake request to be used
environ = create_environ('/home', 'http://127.0.0.1:5000')
request = Request(environ)

# 2. Setup a server and add a Router
server = BaseServer()
server.use_component(Router)


# server.add_route('/home', render_page('index.html'))


@server.as_route('/contact')
def contact(request, **kwargs):
    return render_page(request, 'index.html')


def about(request, **kwargs):
    return render_page(request, 'index.html')


server.add_route('/about', about)


class TestRouting(unittest.TestCase):
    def setUp(self):
        self.router = server.app_options.router

    def test_urls(self):
        self.assertEqual(len(self.router.routes), 2)
        self.assertIsInstance(self.router.routes, Deque)

    def test_first_route(self):
        first_route = self.router.routes[0]
        self.assertIsInstance(first_route, dict)
        self.assertListEqual(
            list(first_route.keys()),
            ['path', 'name', 'view']
        )
        self.assertTrue(callable(first_route['view']))
        self.assertEqual(first_route['path'], '/contact')

    # def test_routing(self):
    #     handler = WSGIRequestHandler(request, '127.0.0.1', server)
    #     r = server.build_request(environ, handler)
    #     print(r)
    #     result = server.dispatch_request(r)
    #     print(result)


if __name__ == '__main__':
    unittest.main()
