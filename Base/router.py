from django.http import HttpRequest
from smartdjango import Error, Code, APIPacker

from Base.handler import BaseHandler
from Model.Base.Config.models import Config


@Error.register
class RouterErrors:
    NOT_FOUND_ROUTE = Error("不存在的API", code=Code.NotFound)
    DISABLED = Error("应用被禁用", code=Code.BadRequest)
    UNAUTHORIZED = Error("没有管理权限", code=Code.Forbidden)


class RouteHandler(BaseHandler):
    APP_NAME = 'router'
    APP_DESC = None

    def __init__(self, router):
        self.SUB_ROUTER = router


class Router:
    def __init__(self):
        self.handlers = dict()
        self.hidden = dict()

    def register(self, path: str, handler, hidden=False):
        self.handlers[path] = handler
        self.hidden[path] = hidden

    def enable(self, path):
        if path in self.handlers:
            self.hidden[path] = False

    def disable(self, path):
        if path in self.handlers:
            self.hidden[path] = True

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

    @property
    def available_handlers(self):
        handlers = {}
        for path in self.handlers:
            if not self.hidden[path]:
                handlers[path] = self.handlers[path]
        return handlers

    @staticmethod
    def authorized(r: HttpRequest):
        # print(r.META)
        return r.META.get('HTTP_TOKEN') == Config.get_value_by_key('StaticToken')

    def route(self, r: HttpRequest, path: str):
        if not path:
            return APIPacker.pack(list(map(self.get_base, self.available_handlers)))

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
                if self.hidden[app_name]:
                    return APIPacker.pack(RouterErrors.DISABLED)
                return handler.run(r)
            elif r.method == 'GET':
                if isinstance(handler, RouteHandler):
                    return APIPacker.pack(list(map(handler.SUB_ROUTER.get_base,
                                                   handler.SUB_ROUTER.available_handlers)))
                return APIPacker.pack(self.get(handler))
            elif r.method in ['PUT', 'DELETE']:
                if not self.authorized(r):
                    return APIPacker.pack(RouterErrors.UNAUTHORIZED)
                if r.method == 'PUT':
                    self.enable(app_name)
                    return APIPacker.pack('应用成功解禁')
                else:
                    self.disable(app_name)
                    return APIPacker.pack('应用成功被禁')
        return APIPacker.pack(RouterErrors.NOT_FOUND_ROUTE)

    def as_handler(self):
        return RouteHandler(self)
