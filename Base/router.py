from SmartDjango import E, Hc, Excp
from django.http import HttpRequest

from Base.handler import BaseHandler


@E.register()
class RouterError:
    NOT_FOUND_ROUTE = E("不存在的API", hc=Hc.NotFound)


class RouteHandler(BaseHandler):
    APP_NAME = 'router'
    APP_DESC = None

    def __init__(self, router):
        self.SUB_ROUTER = router


class Router:
    def __init__(self):
        self.handlers = dict()

    def register(self, path: str, handler):
        self.handlers[path] = handler

    def register_param(self, path: str, handler):
        self.handlers['param:' + path] = handler

    def register_usage(self, path: str, handler):
        self.handlers['usage:' + path] = handler

    @classmethod
    def get(cls, handler: BaseHandler):
        return dict(
            method='POST',
            content_type='application/json',
            app_name=handler.APP_NAME,
            app_desc=handler.APP_DESC,
            params=list(map(handler.readable_param, handler.BODY)),
            example=dict(
                request=handler.REQUEST_EXAMPLE,
                response=handler.RESPONSE_EXAMPLE,
            ),
            sub_router=isinstance(handler.SUB_ROUTER, Router),
        )

    def get_base(self, path):
        handler = self.handlers[path]
        return dict(
            path=path,
            app_name=handler.APP_NAME,
            app_desc=handler.APP_DESC,
        )

    def route(self, r: HttpRequest, path: str):
        if not path:
            return Excp.http_response(list(map(self.get_base, self.handlers)))

        if path.find('/') >= 0:
            app_name = path[:path.find('/')]
            sub_path = path[path.find('/')+1:]
        else:
            app_name = path
            sub_path = None

        if app_name in self.handlers:
            handler = self.handlers[app_name]
            if sub_path is not None and isinstance(handler.SUB_ROUTER, Router):
                return handler.SUB_ROUTER.route(r, sub_path)
            if r.method == 'POST':
                return handler.run(r)
            else:
                if isinstance(handler, RouteHandler):
                    return Excp.http_response(list(map(handler.SUB_ROUTER.get_base, handler.SUB_ROUTER.handlers)))
                return Excp.http_response(self.get(handler))
        return Excp.http_response(RouterError.NOT_FOUND_ROUTE)

    def as_handler(self):
        return RouteHandler(self)
