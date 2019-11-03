from SmartDjango import P, E, Hc


@E.register()
class HandlerError:
    HANDLER_NOT_IMPLEMENTED = E("未实现的功能", hc=Hc.NotImplemented)


class BaseHandler:
    APP_NAME = "应用名称"
    APP_DESC = "应用介绍"

    BODY = []
    # QUERY = []
    REQUEST_EXAMPLE = None
    RESPONSE_EXAMPLE = None

    SUB_ROUTER = None

    @staticmethod
    def run(r):
        return HandlerError.HANDLER_NOT_IMPLEMENTED

    @classmethod
    def readable_param(cls, param: P):
        if isinstance(param, str):
            param = P(param)
        d_ = dict(
            name=param.name,
            desc=param.read_name,
            allow_null=param.allow_null,
            has_default=param.has_default,
            type_='dict' if param.is_dict else 'list' if param.is_list else 'atom',
        )
        if param.has_default:
            d_['default_value'] = param.default_value
            d_['default_through_processors'] = param.default_through_processors
        if param.is_dict:
            d_['dict_fields'] = list(map(cls.readable_param, param.dict_fields))
        if param.is_list and param.list_child:
            d_['list_child'] = cls.readable_param(param.list_child)
        return d_

    def rename(self, app_name=None, app_desc=None):
        self.APP_DESC = app_desc or self.APP_DESC
        self.APP_NAME = app_name or self.APP_NAME
        return self
