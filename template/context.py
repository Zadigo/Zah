from werkzeug.wrappers import Request

class Context(dict):
    def __init__(self, **kwargs):
        super().update(kwargs)
        self.base_context = kwargs

    def __str__(self):
        return str(self.base_context)

    def populate(self, **kwargs):
        for key, value in kwargs.items():
            self.setdefault(key, value)


class RequestContext(Context):
    def __init__(self, request: Request, **kwargs):
        super().__init__(request=request, **kwargs)
