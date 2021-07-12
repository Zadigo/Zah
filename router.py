from collections import deque
from typing import Callable, Dict, List, Tuple, Union

from zah.urls import render


class Router:
    routes = deque()

    @property
    def urls(self):
        # base_api_route = {'path': '/api/v1', 'name': 'api', 'view': render('api.html')}
        # self.routes.append(base_api_route)
        return self.routes

    def add_route(self, path: str, view: Callable, name: str = None):
        """Add a single route to the router"""
        self.routes.append({ 'path': path, 'name': name, 'view': view })
        return self.routes

    def add_url_patterns(self, urls: Union[list, tuple]):
        """Add multiple routes at once to the router"""
        pass

    def match(self, path: str, route_name: str = None) -> Tuple[dict[str, str, Callable], List[dict]]:
        """Match a path or a route name to the registered urls"""
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

        # TODO: When a route is matched, it is added
        # two times in the final list
        candidates = list(filter(matcher, self.routes))
        if len(candidates) >= 1:
            return candidates[0], candidates
        return [], candidates
