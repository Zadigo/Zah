import unittest

from zah.router import Router, reverse_url
from zah.tests.views import items


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = Router()
    
    def test_can_add_route(self):
        self.router.add_route('/', items.home)
        self.assertTrue(len(self.router.urls) > 0)
        
    def test_can_match_route(self):
        candidate, candidates = self.router.match('/')
        self.assertTrue(candidate['path'] == '/')
        self.assertTrue(len(candidates) > 0)
        
    def test_can_match_by_name(self):
        self.router.add_route('/home', items.home, name='home')
        candidate, candidates = self.router.match('/', 'home')
        self.assertTrue(candidate['path'] == '/')
        self.assertTrue(len(candidates) > 0)
    
    def test_can_reverse_url_in_router(self):
        path = reverse_url('home')
        self.assertIsNotNone(path)
        self.assertEqual(path, '/home')
        
        
if __name__ == '__main__':
    unittest.main()
        
