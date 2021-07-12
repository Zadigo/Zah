from collections import deque
from typing import Callable, List, Tuple, Type, Union


class Router:
    routes = deque()

    @property
    def urls(self):
        # base_api_route = {'path': '/api/v1', 'name': 'api', 'view': render('api.html')}
        # self.routes.append(base_api_route)
        return self.routes

    @classmethod
    def copy(cls):
        routes = cls.routes.copy()
        instance = cls()
        instance.routes = routes
        return instance

    def add_route(self, path: str, view: Callable, name: str = None):
        """Add a single route to the router"""
        self.routes.append({ 'path': path, 'name': name, 'view': view })
        return self.routes

    def add_url_patterns(self, urls: Union[list, tuple]):
        """Add multiple routes at once to the router"""
        for url in urls:
            if not callable(url):
                raise TypeError('Url should be a callable')
            self.add_route(**url)

    def match(self, path: str, route_name: str = None) -> Tuple[dict[str, str, Callable], List[dict]]:
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

        # TODO: When a route is matched, it is added
        # two times in the final list
        candidates = list(filter(matcher, self.routes))
        if len(candidates) >= 1:
            return candidates[0], candidates
        return [], candidates

    # def match_from_name(self, route_name: str) -> Tuple[dict[str, str, Callable], List[dict]]:
    #     pass


def reverse_url(name: str) -> Union[str, None]:
    # TODO:
    router = Router.copy()
    candidate, _ = router.match(route_name=name)
    if not candidate:
        return None
    return candidate['path']
