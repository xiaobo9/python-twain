
import logging
from functools import wraps

logger = logging.getLogger('route_func')

routes = {}


def route(*args, **kwargs):
    """
    路由
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        path = kwargs["path"]
        if isinstance(path, list):
            for p in path:
                routes[p] = wrapper
        elif isinstance(path, str):
            routes[path] = wrapper

        return wrapper
    return decorator


def simple_router(path):
    # logger.debug("path: [%s]",path)
    if path in routes:
        return routes[path]
    # logger.info("404")
    return None


if __name__ == '__main__':
    print('route_func.py')

    @route(path=['/', '/index', '/index.html'])
    def index(path):
        print(f'path: {path}')
        return 'index.html'

    @route(path=['/api/scan'])
    def api_scan(path):
        print(f'path: {path}')
        return '/api/scan'

    path = '/index'
    simple_router(path)(path)
    path = '/api/scan'
    simple_router(path)(path)
    path = '/404.html'
    simple_router(path)(path)
