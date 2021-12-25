import unittest
from werkzeug.wrappers import Request
from werkzeug.serving import WSGIRequestHandler
from werkzeug.test import create_environ
from zah.tests.views import items

environ = create_environ('/', 'http://127.0.0.1:5000')
request = Request(environ)

def start_response(status, headers, exec_info=None):
    pass 

# home() -> render ==> HTTPResponse

class TestViewFunction(unittest.TestCase):
    def test_renders_template(self):
        render_function = items.home(request)
        # The response object returns a ClosingIterator
        # object which contains the string of the template
        result = list(render_function(environ, start_response))
        self.assertTrue(len(result) > 0)




# from werkzeug.test import create_environ
# from werkzeug.wrappers import Request
# from zah.decorators._http import only_GET
# from zah.responses import HttpResponse
# from zah.urls import render

# environ = create_environ('/home', 'http://127.0.0.1:5000')
# request = Request(environ)

# # home() -> render ==> HttpResponse


# def home(request, **kwargs):
#     return render(request, 'home.html')

# # only_GET(home)() -> view -> view() -> render ==> HttpResponse


# @only_GET
# def contact(request, **kwargs):
#     return render(request, 'home.html')


# class TestViews(unittest.TestCase):
#     def test_rendering_process(self):
#         response = home(request)
#         self.assertIsInstance(response, HttpResponse)

#     def test_rendering_process_with_decorator(self):
#         response = contact(request)
#         self.assertIsInstance(response, HttpResponse)


if __name__ == '__main__':
    unittest.main()
