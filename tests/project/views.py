from zah.urls import render


def home(request, **kwargs):
    return render(request, 'home.html')
