import importlib
import unittest

from zah.apps.registry import Apps

apps = Apps()

class TestApps(unittest.TestCase):
    def setUp(self):
        router_module = importlib.import_module('zah.router.app')
        apps.register(router_module, getattr(router_module, 'Router')())

    def test_can_get_app(self):
        result = apps.get_app_by_name('router')
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_can_get_app_instance(self):
        from zah.router.app import Router
        router = apps.get_app_instance('router')
        self.assertIsInstance(router, Router)
        
if __name__ == '__main__':
    unittest.main()
