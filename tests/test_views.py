import unittest

from werkzeug.test import create_environ
from werkzeug.wrappers import Request
from zah.responses import HttpResponse
from zah.urls import render
from zah.decorators import only_GET

environ = create_environ('/home', 'http://127.0.0.1:5000')
request = Request(environ)

# home() -> render ==> HttpResponse

def home(request, **kwargs):
    return render(request, 'home.html')

# only_GET(home)() -> view -> view() -> render ==> HttpResponse

@only_GET
def contact(request, **kwargs):
    return render(request, 'home.html')

class TestViews(unittest.TestCase):
    def test_rendering_process(self):
        response = home(request)
        self.assertIsInstance(response, HttpResponse)

    def test_rendering_process_with_decorator(self):
        response = contact(request)
        self.assertIsInstance(response, HttpResponse)
        

if __name__ == '__main__':
    unittest.main()
