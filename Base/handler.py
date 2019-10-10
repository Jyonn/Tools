from SmartDjango import P, E, ErrorJar


@ErrorJar.pour
class HandlerError:
    HANDLER_NOT_IMPLEMENTED = E("未实现的功能")


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
            allow_null=param.null,
            has_default=param.has_default(),
            is_dict=param.dict,
            is_list=param.list,
            children=list(map(cls.readable_param, param.children))
        )
        if param.has_default():
            d_['default_value'] = param.default
        return d_

    def rename(self, app_name=None, app_desc=None):
        self.APP_DESC = app_desc or self.APP_DESC
        self.APP_NAME = app_name or self.APP_NAME
        return self
