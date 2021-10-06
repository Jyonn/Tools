from functools import wraps
from hashlib import md5

from SmartDjango import E

from dev.Arts.Foto.base import ADMIN_TOKEN


@E.register(id_processor=E.idp_cls_prefix())
class AuthError:
    ADMIN = E("需要管理员身份登录")


class Auth:
    @staticmethod
    def get_md5(s):
        m = md5()
        m.update(s.encode())
        return m.hexdigest()

    @classmethod
    def validate_token(cls, request):
        token = request.META.get('HTTP_TOKEN')
        if not token or cls.get_md5(token) != ADMIN_TOKEN:
            raise AuthError.ADMIN

    @classmethod
    def require_admin(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            cls.validate_token(r)
            return func(r, *args, **kwargs)

        return wrapper
