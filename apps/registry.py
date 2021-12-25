from zah.utils.iteration import keep_while


# class AppModule:
#     MODULE = None
    
#     def __init__(self, module, instance):
#         self.MODULE = module
#         self.dotted_path = self.MODULE.__path__
        


class Apps:
    """Stores the apps that are requied for
    the given project"""

    registry = set()

    def __repr__(self):
        return f"{self.__class__.__name__}(apps={len(self.registry)})"

    def register(self, module, instance):
        """Register an application to the registry"""
        self.registry.add((module, instance, instance.verbose_name))

    def get_app_by_name(self, name):
        candidates = keep_while(lambda x: name in x, self.registry)
        return list(candidates)

    def get_app_instance(self, name):
        candidates = self.get_app_by_name(name)
        if candidates:
            candidate = candidates[0]
            _, instance, _ = candidate
            return instance
        raise KeyError('App does not exist')
