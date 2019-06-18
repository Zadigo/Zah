from werkzeug.serving import run_simple

from zah.base import Zah
from zah.core.shortcuts import render

app = Zah(__file__)

def home(request):
    return render(request, 'base.htm')

# def contact(request):
#     return render(request, 'contact.htm')

app.router.add_route('/', home, 'home')
# app.router.add_route('/contact', contact, 'contact')



# run_simple('127.0.0.1', 8080, app.wsgi_app, use_debugger=True, use_reloader=True)
