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

class TestRequests(unittest.TestCase):
    def setUp(self):
        server.add_route('/home', render_page('home.html'))

    def test_returns_http_response(self):
        response = server._dispatch_request(request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
