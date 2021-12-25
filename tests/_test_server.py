from core.servers import DevelopmentServer
from zah.core.servers import BaseServer
from zah.decorators._cache import cache_control, never_cache
from zah.decorators._http import only_SAFE
from zah.router import Router
from zah.store import BaseModule
from zah.urls import render, render_page

server = BaseServer()
# server = DevelopmentServer()
server.use_component(Router)

@cache_control(max_age=30)
def home(request, **kwargs):
    return render(request, 'api.html')


@never_cache
def about(request, **kwargs):
    return render(request, 'api.html')


server.add_route('/', render_page('home.html'))
server.add_route('/home', home, name='home')
server.add_route('/about', about, name='about')

server.create()
