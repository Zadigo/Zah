from zah.store import BaseModule
from zah.server import BaseServer
from zah.urls import render, render_page
from zah.router import Router
from zah.decorators import only_SAFE

server = BaseServer()
server.use_component(Router)
server.add_route('/', render_page('home.html'))

@only_SAFE
def home(request, **kwargs):
    return render(request, 'api.html')

server.add_route('/home', home, name='home')

server.create()
