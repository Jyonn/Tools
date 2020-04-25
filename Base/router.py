from SmartDjango import E, Hc, NetPacker
from django.http import HttpRequest

from Base.handler import BaseHandler
from Model.Base.Config.models import Config


@E.register()
class RouterError:
    NOT_FOUND_ROUTE = E("不存在的API", hc=Hc.NotFound)
    DISABLED = E("应用被禁用")
    UNAUTHORIZED = E("没有管理权限")


class RouteHandler(BaseHandler):
    APP_NAME = 'router'
    APP_DESC = None

    def __init__(self, router):
        self.SUB_ROUTER = router


class Router:
    def __init__(self):
        self.handlers = dict()
        self.disabled = dict()

    def register(self, path: str, handler, disabled=False):
        self.handlers[path] = handler
        self.disabled[path] = disabled

    def enable(self, path):
        if path in self.handlers:
            self.disabled[path] = False

    def disable(self, path):
        if path in self.handlers:
            self.disabled[path] = True

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
            if not self.disabled[path]:
                handlers[path] = self.handlers[path]
        return handlers

    @staticmethod
    def authorized(r: HttpRequest):
        print(r.META)
        return r.META.get('HTTP_TOKEN') == Config.get_value_by_key('StaticToken')

    def route(self, r: HttpRequest, path: str):
        if not path:
            return NetPacker.send(list(map(self.get_base, self.available_handlers)))

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
                if self.disabled[app_name]:
                    return NetPacker.send(RouterError.DISABLED)
                return handler.run(r)
            elif r.method == 'GET':
                if isinstance(handler, RouteHandler):
                    return NetPacker.send(list(map(handler.SUB_ROUTER.get_base,
                                                   handler.SUB_ROUTER.available_handlers)))
                return NetPacker.send(self.get(handler))
            elif r.method in ['PUT', 'DELETE']:
                if not self.authorized(r):
                    return NetPacker.send(RouterError.UNAUTHORIZED)
                if r.method == 'PUT':
                    self.enable(app_name)
                    return NetPacker.send('应用成功解禁')
                else:
                    self.disable(app_name)
                    return NetPacker.send('应用成功被禁')
        return NetPacker.send(RouterError.NOT_FOUND_ROUTE)

    def as_handler(self):
        return RouteHandler(self)
