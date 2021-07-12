from web.store import BaseModule
from web.server import BaseServer
from web.urls import render, render_page
from web.router import Router
from web.decorators import only_SAFE

server = BaseServer()
server.use_component(Router)
server.add_route('/', render_page('home.html'))

@only_SAFE
def home(request, **kwargs):
    return render(request, 'api.html')

server.add_route('/home', home, name='home')

server.create()
