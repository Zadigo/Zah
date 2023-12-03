class Context(dict):
    """A wrapper that passes context data
    to the application

    >>> context = Context()
    """

    def __init__(self, **kwargs):
        super().update(kwargs)
        self.base_context = kwargs

    def __str__(self):
        return str(self.base_context)

    def populate(self, **kwargs):
        for key, value in kwargs.items():
            self.setdefault(key, value)


class RequestContext(Context):
    """A wrapper that passes context data
    in addition to the current request
    to a template

    >>> context = RequestContext()
    """

    def __init__(self, request, **kwargs):
        super().__init__(request=request, **kwargs)
