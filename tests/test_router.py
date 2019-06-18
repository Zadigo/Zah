import unittest
from zah.core.router import DefaultRouter
from zah.core.shortcuts import render

# Basic view function
def home(request):
    return render(request, 'base.htm')

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = DefaultRouter()

    def test_is_dict(self):
        self.assertTrue(isinstance(self.router.routes, dict))

    def test_adding_routes(self):
        self.router.add_route('home', home, 'home')
        expected_object = {'home': {'path': 'home', 'view': home, 'context': {}}}
        self.assertDictEqual(self.router.routes, expected_object)

    def test_multiple_routes(self):
        self.router.add_route('home', home, 'home')
        self.router.add_route('page/contact/', home, 'contact')

        self.assertEqual(len(self.router.routes), 2)

    def test_returned_route_correct(self):
        self.router.add_route('home', home, 'home')
        route = self.router.match_route('home')
        # path should be equal to home
        self.assertEqual(route['path'], 'home')

    def test_render_function(self):
        self.router.add_route('home', home, 'home')
        route = self.router.match_route('home')
        # View should a callable
        self.assertTrue(callable(route['view']))
        
        view_function = route['view']
        # {} is request
        # Should get view callable
        self.assertEqual(view_function({}).__name__, 'view')
        # Should get html string
        self.assertEqual(type(view_function({})()), str)
        

if __name__ == "__main__":
    unittest.main()
