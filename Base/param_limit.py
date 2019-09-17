from SmartDjango import BaseError, Excp


class ParamLimit:
    @staticmethod
    def str_len(max_len, min_len=0):
        @Excp.pack
        def decorator(string):
            if not isinstance(string, str):
                return BaseError.FIELD_FORMAT
            if len(string) < min_len or len(string) > max_len:
                return BaseError.FIELD_FORMAT
        return decorator

    @staticmethod
    def choices(choices):
        @Excp.pack
        def decorator(value):
            if value not in choices:
                return BaseError.FIELD_FORMAT
        return decorator

    @staticmethod
    def number(max_, min_=0):
        @Excp.pack
        def decorator(value):
            if value > max_:
                value = max_
            if value < min_:
                value = min_
            return value
        return decorator


PL = ParamLimit
