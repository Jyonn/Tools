from SmartDjango import Packing, Param


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
        _d = dict(
            name=param.name,
            desc=param.verbose_name,
            allow_null=param.allow_null,
            has_default=param.has_default(),
        )
        if param.has_default():
            _d['default_value'] = param.default_value
        return _d

    @staticmethod
    @Packing.http_pack
    def get(r):
        return dict(
            app_name=cls.APP_NAME,
            app_desc=cls.APP_DESC,
            body_params=list(map(cls.readable_param, cls.BODY)),
            query_params=list(map(cls.readable_param, cls.QUERY)),
        )
