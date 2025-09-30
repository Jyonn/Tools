from functools import wraps
from hashlib import md5

from smartdjango import Error, Code, analyse

from dev.Arts.Foto.base import ADMIN_TOKEN


@Error.register
class AuthErrors:
    ADMIN = Error("需要管理员身份登录", code=Code.Forbidden)


def get_md5(s):
    m = md5()
    m.update(s.encode())
    return m.hexdigest()


def validate_token(request):
    token = request.META.get('HTTP_TOKEN')
    if not token or get_md5(token) != ADMIN_TOKEN:
        raise AuthErrors.ADMIN


def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = analyse.get_request(*args)
        validate_token(request)
        return func(*args, **kwargs)

    return wrapper
