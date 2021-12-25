import unittest

from werkzeug.test import create_environ
from werkzeug.wrappers import Request
from zah.decorators import only_GET
from zah.responses import HttpResponse
from zah.router import Router
from zah.server import BaseServer
from zah.urls import render, render_page

# 1. Create a fake request to be used

environ = create_environ('/home', 'http://127.0.0.1:5000')
request = Request(environ)

# 2. Setup a server and add a Router

server = BaseServer()
server.use_component(Router)

server.add_route('/home', render_page('home.html'))


@server.as_route('/contact')
def contact(request, **kwargs):
    return render(request, 'home.html')


def about(request, **kwargs):
    return render(request, 'home.html')
server.add_route('/about', about)


class TestRouting(unittest.TestCase):
    def setUp(self):
        self.router = server.app_descriptor.apps['router']

    def test_urls(self):
        self.assertEqual(len(self.router.routes), 3)

    def test_first_route(self):
        first_route = self.router.routes[0]
        self.assertIsInstance(first_route, dict)
        self.assertEqual(first_route['path'], '/home')


if __name__ == '__main__':
    unittest.main()
