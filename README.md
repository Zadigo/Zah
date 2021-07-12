# Zah

A lightweight web framework that works and hand in hand with VueJS.

Zah serves as a backend for your VueJS application.

# Getting started

Creating a Zah website is as simple as the following:

```
from zah.server import BaseServer

server = BaseServer()
server.create()
```

The `create` method will create a new instanace of the BaseServer class and pass it through Werkzeug.

### Parameters

__Host__ 

__Port__

# Using applications

Zah comes with a set of none integrate default apps that can be used for various purposes. To use these applications, you have to actively tell Zah to integrate remember them in the `Descriptor`. Once these apps are intergrated, they become automatically accessible within your templates and throughout your application.

```
class Component:
    pass

server.use_component(Component)
```

# Routing

While the main purpose of Zah is to serve as a backbone for your Vue application, you can still create routes to classic Jinja2 based HTML files if you wish to. There are three techniques.

Zah was created as way to only include what you need and for that matter, since VueJS apps are SPA's and do not require backend routing, there is no router by default.

To implement backend routing just like you would do for any other application do:

```
from zah.router import Router

server.use_component(Router)
server.add_route('/', render_page('home.html'))
```

## Simple route

```
from zah.urls import render_page

server.add_route('/', 'home.html', name='home')
```

This is the most basic and simple way to render a page with Zah. The `add_route` method's only purpose is to render a page that does not require complex logic. This is is very ideal for rendering for example the `index.html` file of the VueJS framework.

## Decorated route

If you need more complex logic within your route, you can use the `as_route` decorator.

```
@server.as_route('/home')
def home(request, **kwargs):
    return render(request, 'home.html')
```

This technique is very similar to the following

```
def home(request, **kwargs):
    return render(request, 'home.html')

server.add_route('/', home, name='home')
```

# Decorators

## HTTP

You can decorate your routes with very specific decorators that will limit, restrict or modify the response or the request.

```
from zah.decorators import only_GET

@only_GET
def home(request, **kwargs):
    return render(request, 'home.html', context)
```

A similar approach can be used using `render_page`.

```
server.add_route('/about', only_GET(render_page('about.html')))
```
