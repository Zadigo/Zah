from zah.router.app import Router
# from zah.store import Store
from zah.urls import render, render_page
from zah.core.servers import BaseServer, DevelopmentServer
from zah.shortcuts import get_default_server

app = BaseServer()
# app = get_default_server()
# app.use_component(Router)
# app.use_component(Store)

# def view1(request, **kwargs):
#     return render(request, 'home.html')

# @app.as_route('/test2', 'test2')
# def view2(request, **kwargs):
#     return render(request, 'home.html')

# app.add_route('/test', view1, 'test1')
# app.add_route('/test3', render_page('home.html'))
