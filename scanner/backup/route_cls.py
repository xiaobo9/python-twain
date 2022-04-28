
import logging
from functools import wraps

logger = logging.getLogger('route_cls')


class route():
    routes = {}
    route_404 = None
    """
    路由
    """

    def __init__(self, *args, **kwargs):
        self.path = kwargs['path']

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        path = self.path
        if isinstance(path, list):
            for p in path:
                route.routes[p] = wrapper
        elif isinstance(path, str):
            route.routes[path] = wrapper

        return wrapper

    @classmethod
    def router(cls, path):
        """
        根据 path 获取路由接口
        """
        # logger.debug("path: [%s]",path)
        if path in route.routes:
            return route.routes[path]
        if route.route_404:
            return route.route_404
        return None


if __name__ == '__main__':
    print('测试代码 route_cls.py')

    class Handler():
        def __init__(self, *args, **kwargs):
            self.path = args[0]

        def handle(self):
            api = route.router(self.path)
            if api:
                return api(self)
            else:
                print('none')
                return self.error_404()

        @route(path=['/', '/index', '/index.html'])
        def index(self):
            result = f'index, path: {self.path}'
            return result

        @route(path=['/api/scan'])
        def api_scan(self):
            result = f'api_scan, path: {self.path}'
            return result

        @route(path=['404'])
        def error_404(self):
            result = f'error_404, path: {self.path}'
            return result

    route.route_404 = Handler.error_404

    assert 'index, path: /index' == Handler('/index').handle()
    assert 'api_scan, path: /api/scan' == Handler('/api/scan').handle()
    assert 'error_404, path: 404' == Handler('404').handle()
    assert 'error_404, path: /user.html' == Handler('/user.html').handle()
