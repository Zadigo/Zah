from web.router import Router
from web.urls import render, static, url
from werkzeug.wrappers import Request
from web.decorators import only_GET, only_http_methods

request = Request({})

router = Router()
# router.add_route('/', render('home.html'))
# router.add_route('/api', render('api.html'), name='home')
# candidate, candidates = router.match('/api')
# view = candidate['view'](request=request)

# routes = [
#     url('/', render('home.html'), name='google')
# ]

# router.add_url_patterns(routes)


# @router.as_route('/home')
# def home(request, **kwargs):
#     return render('home.html', request=request)

# print(router.urls)


@only_GET
def home(request, **kwargs):
    return render('home.html', request=request)
from web import server_configuration

static(server_configuration.BASE_PATH, '/static')
