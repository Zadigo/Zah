from zah.urls import render
from zah.decorators._http import only_GET, only_POST, only_SAFE
from zah.decorators._cache import cache_page, never_cache

def home(request, **kwargs):
    return render(request, 'home.html')


@only_GET
def home1(request, **kwargs):
    return render(request, 'home.html')


@only_POST
def home2(request, **kwargs):
    return render(request, 'home.html')


@only_SAFE
def home3(request, **kwargs):
    return render(request, 'home.html')


@never_cache
def home4(request, **kwargs):
    return render(request, 'home.html')


@cache_page
def home5(request, **kwargs):
    return render(request, 'home.html')
