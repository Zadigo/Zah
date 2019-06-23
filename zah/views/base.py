from zah.core.shortcuts import render

class BaseView:
    methods = ['get', 'post']
    template = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, template)

    def post(self, request, **kwargs):
        return render(request, template)

    @classmethod
    def to_view(cls, **kwargs):
        if '' == 'GET':
            cls.get(request)

class View(BaseView):
    pass