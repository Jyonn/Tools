from SmartDjango import Excp, ErrorCenter, E
from django.http import HttpRequest


class RouterError(ErrorCenter):
    NOT_FOUND_ROUTE = E("不存在的API", hc=404)


RouterError.register()


class Router:
    def __init__(self):
        self.handlers = dict()

    def register(self, path: str, handler):
        self.handlers[path] = handler

    @classmethod
    def get(cls, handler):
        return dict(
            method='POST',
            app_name=handler.APP_NAME,
            app_desc=handler.APP_DESC,
            body_params=list(map(handler.readable_param, handler.BODY)),
            query_params=list(map(handler.readable_param, handler.QUERY))
        )

    def get_base(self, path):
        handler = self.handlers[path]
        return dict(
            path=path,
            app_name=handler.APP_NAME,
            app_desc=handler.APP_DESC,
        )

    def route(self, r: HttpRequest, path):
        if not path:
            return Excp.http_response(list(map(self.get_base, self.handlers)))

        if path in self.handlers:
            handler = self.handlers[path]
            if r.method == 'POST':
                return handler.run(r)
            else:
                return Excp.http_response(self.get(handler))
        return Excp.http_response(RouterError.NOT_FOUND_ROUTE)
