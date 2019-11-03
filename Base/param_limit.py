from SmartDjango.models.base import ModelError


class ParamLimit:
    @staticmethod
    def str_len(max_len, min_len=0):
        def decorator(string):
            if not isinstance(string, str):
                raise ModelError.FIELD_FORMAT
            if len(string) < min_len or len(string) > max_len:
                raise ModelError.FIELD_FORMAT
        return decorator

    @staticmethod
    def choices(choices):
        def decorator(value):
            if value not in choices:
                raise ModelError.FIELD_FORMAT
        return decorator

    @staticmethod
    def number(max_, min_=0):
        def decorator(value):
            if value > max_:
                value = max_
            if value < min_:
                value = min_
            return value
        return decorator

    @staticmethod
    def ip_dot2int(ip: str):
        ip_seg = ip.split('.')
        if len(ip_seg) != 4:
            raise ModelError.FIELD_FORMAT('IP地址格式错误')
        ip_seg = list(map(int, ip_seg))
        ip_number = 0

        for seg in ip_seg:
            if seg < 0 or seg > 255:
                raise ModelError.FIELD_FORMAT('IP地址格式错误')
            ip_number <<= 8
            ip_number += seg

        return ip_number


PL = ParamLimit
