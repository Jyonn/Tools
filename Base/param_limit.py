from SmartDjango import BaseError, Packing


class ParamLimit:
    @staticmethod
    def str_len(max_len, min_len=0):
        @Packing.pack
        def decorator(string):
            if not isinstance(string, str):
                return BaseError.FIELD_FORMAT
            if len(string) < min_len or len(string) > max_len:
                return BaseError.FIELD_FORMAT


PL = ParamLimit
