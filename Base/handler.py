from SmartDjango import Param


class BaseHandler:
    APP_NAME = "应用名称"
    APP_DESC = "应用介绍"
    BODY = []
    QUERY = []

    @staticmethod
    def run():
        pass

    @classmethod
    def readable_param(cls, param: Param):
        d_ = dict(
            name=param.name,
            desc=param.read_name,
            allow_null=param.null,
            has_default=param.has_default(),
        )
        if param.has_default():
            d_['default_value'] = param.default
        return d_
