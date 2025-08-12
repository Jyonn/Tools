from typing import cast

from smartdjango import Error, Code, Validator, DictValidator, ListValidator


@Error.register
class HandlerErrors:
    HANDLER_NOT_IMPLEMENTED = Error("未实现的功能", code=Code.NotImplemented)


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
        return HandlerErrors.HANDLER_NOT_IMPLEMENTED

    @classmethod
    def readable_param(cls, param: Validator):
        if isinstance(param, str):
            param = Validator(param)

        has_default = param.default_value != getattr(param, "_Validator__NoDefaultValue", None)
        is_dict = isinstance(param, DictValidator)
        is_list = isinstance(param, ListValidator)
        d_ = dict(
            name=param.key.name,
            desc=param.key.verbose_name,
            allow_null=param.allow_null,
            has_default=has_default,
            type_='dict' if is_dict else 'list' if is_list else 'atom',
        )
        if has_default:
            d_['default_value'] = param.default_value
        if is_dict:
            d_['dict_fields'] = list(map(cls.readable_param, param.dict_fields))
        if is_list and cast(ListValidator, param).element_validator:
            d_['list_child'] = cls.readable_param(cast(ListValidator, param).element_validator)
        return d_

    def rename(self, app_name=None, app_desc=None):
        self.APP_DESC = app_desc or self.APP_DESC
        self.APP_NAME = app_name or self.APP_NAME
        return self
