from router import reverse_url
import unittest

from zah.router import Router
from zah.server import BaseServer
from zah.urls import render_page

server = BaseServer()
server.use_component(Router)

class TestRouter(unittest.TestCase):
    def setUp(self):
        server.add_route('/home', render_page('home.html'))
        self.router = server.app_descriptor.apps['router']

    def test_has_routes(self):
        self.assertGreaterEqual(len(self.router.routes), 1)

    def test_has_route(self):
        # Expected tuple(dict, list)
        result = self.router.match(path='/home')
        self.assertIsInstance(result, tuple)
        candidate, candidates = result
        
        self.assertIsInstance(candidate, dict)
        self.assertEqual(candidate['path'], '/home')


class TestRouterUtils(unittest.TestCase):
    def setUp(self):
        server.add_route('/home', render_page('home.html'), name='home')
        self.router = server.app_descriptor.apps['router']

    def test_reverse_url(self):
        # From a given url name,
        # get the path of a url
        result = reverse_url('home')
        self.assertIsNotNone(result)
        self.assertEqual(result, '/home')


if __name__ == '__main__':
    unittest.main()
