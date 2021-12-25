# from zah.router import Router
# from zah.urls import render
# from zah.router import reverse_url

# router = Router()

# def some_view(request, **kwargs):
#     return render(request, 'home.html')

# router.add_route('/home', some_view, 'home')

# print(reverse_url('home'))

import werkzeug
from zah.utils.servers import BaseServer, start_project
from zah.urls import render
from zah.router import Router

class MyServer(BaseServer):
    pass

t = MyServer()
t.use_component(Router)
def some_view(request):
    return render(request, 'home.html')
t.add_route('/test', some_view, name='test')
t.create()
# t.create()
# werkzeug.run_simple('127.0.0.1', 8000, t.app)
# start_project(t)
