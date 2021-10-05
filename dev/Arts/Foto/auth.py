from functools import wraps

from SmartDjango import E

from dev.Arts.Foto.base import ADMIN_TOKEN


@E.register(id_processor=E.idp_cls_prefix())
class AuthError:
    ADMIN = E("需要管理员身份登录")


class Auth:
    @staticmethod
    def validate_token(request):
        token = request.META.get('HTTP_TOKEN')
        if token != ADMIN_TOKEN:
            raise AuthError.ADMIN

    @classmethod
    def require_admin(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            cls.validate_token(r)
            r.spaceman = r.d.image.get_member(r.user)
            return func(r, *args, **kwargs)

        return wrapper
