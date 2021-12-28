from typing import Union
from zah.apps import apps
from zah.router.shortcuts import get_router

def get_router():
    try:
        router = apps.get_app_instance('router')
    except:
        from zah.router.app import Router
        router = Router()
    return router


def reverse_url(name: str) -> Union[str, None]:
    # from zah.router.app import Router
    
    # router = Router.copy()
    router = get_router()
    candidates = list(router.match_from_name(name))
    if not candidates:
        return None

    candidate = candidates[0]
    if not candidate:
        return None
    return candidate['path']
