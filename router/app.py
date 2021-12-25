from collections import deque
from typing import Callable, List, Tuple, Union

class Router:
    """An application that stores all the given
    routes for a project
    
    NOTE: This is not required to be setup by default since Vue only
    requires one route '/' for the 'index.html' file. Therefore
    the user can choose to implement additionnal routes"""
    
    verbose_name = 'router'
    routes = deque()
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.routes})"
    
    def __iter__(self):
        return iter(self.routes)
    
    def __len__(self):
        return len(self.routes)

    @property
    def urls(self):
        return self.routes

    @classmethod
    def copy(cls):
        routes = cls.routes.copy()
        instance = cls()
        instance.routes = routes
        return instance
    
    def has_path(self, path):
        items = list(filter(lambda x: x['path'] == path, self.urls))
        return len(items) > 0

    def add_route(self, path: str, view: Callable, name: str = None):
        """Add a single route to the router"""
        if path is None:
            raise ValueError('Path should be a valid string')
        
        if path == '':
            path = '/'
            
        self.routes.append({ 'path': path, 'name': name, 'view': view })
        return self.routes

    def add_url_patterns(self, urls: Union[list, tuple]):
        """Add multiple routes at once to the router"""
        for url in urls:
            if not callable(url):
                raise TypeError('Url should be a callable')
            self.add_route(**url)

    def match(self, path: str, route_name: str=None) -> Tuple[dict[str, str, Callable], List[dict]]:
        """Get a url using a path and enventually a router name"""
        def matcher(route_dict: dict):
            registered_path = route_dict.get('path', None)
            if registered_path is not None:
                if path == registered_path or path in registered_path:
                    return True

            if route_name is None:
                return False

            registered_name = route_dict.get('name', None)
            if registered_name is not None:
                if route_name == registered_name or route_name in registered_name:
                    return True
            return False
        
        candidates = list(filter(matcher, self.routes))
        if len(candidates) >= 1:
            return candidates[0], candidates
        return [], candidates

    def match_from_name(self, route_name: str):
        def matcher(item):
            if item['name'] is None:
                return False
            return item['name'] == route_name
        return filter(matcher, self.urls)
