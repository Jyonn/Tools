from SmartDjango import BaseError, Excp


class ParamLimit:
    @staticmethod
    def str_len(max_len, min_len=0):
        @Excp.pack
        def decorator(string):
            print('hi')
            if not isinstance(string, str):
                return BaseError.FIELD_FORMAT
            if len(string) < min_len or len(string) > max_len:
                return BaseError.FIELD_FORMAT
        return decorator


PL = ParamLimit
