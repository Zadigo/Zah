from web.router import Router
from web.server import BaseServer
from web.urls import render, render_page
from werkzeug.test import create_environ
from web.decorators import only_GET
from werkzeug.wrappers import Request

environ = create_environ('/home', 'http://127.0.0.1:5000')
request = Request(environ)

server = BaseServer()
server.use_component(Router)

# 1. Using render page
# server.add_route('/home', render_page('home.html'))

# 2. Using decorator
@server.as_route('/contact')
def contact(request, **kwargs):
    return render(request, 'home.html')

# 3. Using view function
# @only_SAFE
# def home(request, *args, **kwargs):
#     return render(request, 'home.html')
# server.add_route('/home', home)

# print(request.headers)
# response = server._dispatch_request(request)
# try:
#     print(response)
# except:
#     print(response, '/ has no headers')
