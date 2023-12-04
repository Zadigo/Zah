from zah.core.servers import BaseServer, DevelopmentServer
from zah.router import Router
from zah.urls.base import render_page
from zah.conf import settings

app = BaseServer()
app.use_component(Router)


class MyComponent:
    def __call__(self, simple_app):
        pass


@app.as_route('/')
def first_view(request, **kwargs):
    return render_page('index.html')


@app.as_route('/2')
def second_view(request, **kwargs):
    return render_page('index2.html')


app.use_component(MyComponent)
app.create()
