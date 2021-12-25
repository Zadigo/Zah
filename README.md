# Zah

A lightweight web framework that works and hand in hand with VueJS.

Zah serves as a backend for your VueJS application.

## Getting started

Creating a Zah website is as simple as the following:

```python
from zah.server import BaseServer

server = BaseServer()
server.create()
```

The `create` method will create a new instance of the BaseServer class and pass it through Werkzeug.

## Starting a project

### Using applications

Zah comes with a set of none integrated default apps that can be used for various purposes. To use these applications, you have to actively tell Zah integrate them via the `AppOptions` class.

Once these apps are intergrated, they become automatically accessible within your templates and throughout your application.

```python
class Component:
    pass

server.use_component(Component)
```

### Routing

While the main purpose of Zah is to serve as a backbone for your Vue application, you can still create routes to classic Jinja2 based HTML files if you wish to. There are three techniques.

Zah was created as way to only include what you need and for that matter, since VueJS apps are SPA's and do not require backend routing, there is no router by default.

To implement backend routing just like you would do for any other application do:

```python
from zah.router.app import Router

server.use_component(Router)
server.add_route('/', render_page('home.html'))
```

Or in your settings file:

```python
APPS = [
    'zah.router.app.Router'
]
```

#### Simple route

```python
from zah.urls import render_page

server.add_route('/', render_page('home.html'))
```

This is the most basic and simple way to render a page. This is is very ideal for rendering for example the `index.html` file of the VueJS framework.

#### Decorated route

If you need more complex logic within your view, you can use the `as_route` decorator.

```python
@server.as_route('/home')
def home(request, **kwargs):
    return render(request, 'home.html')
```

#### Complex views

In the same manner, if you need more complexe logic within your route, you can also create a view and then pass it to the `add_route` method of the server.

```python
def home(request, **kwargs):
    return render(request, 'home.html')

server.add_route('/', home, name='home')
```

#### Urls file

A final and more efficient way of creating multiple routes for your project can ba done by using a `urls.py` file which will be automatically loaded on project startup. The `urls.py` file requires a `patterns` attribute or it will raise an exception.

```python
from zah.urls import url 
from zah.views import home

patterns = [
    url('/', home, name='home')
]
```

## Decorators

### HTTP

You can decorate your routes with very specific decorators that will limit, restrict or modify the response or the request.

#### only_GET decorator

Requires that only GET HTTP method be treated by this view.

```python
from zah.decorators import only_GET

@only_GET
def home(request, **kwargs):
    return render(request, 'home.html', context)
```

A similar approach can be used using `render_page`.

```python
server.add_route('/about', only_GET(render_page('about.html')))
```

## Applications

### Router

## Database

## Commands

## Settings

### Overview

### Full list of settings

#### Host

#### Port
