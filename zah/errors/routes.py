class RouteError(Exception):
    pass

class RequestParameterException(TypeError):
    def __init__(self):
        pass

    def __str__(self):
        return 'ERROR'

    def __unicode__(self):
        return self.__str__()