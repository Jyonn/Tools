from smartdjango import Error, Code


@Error.register
class VPNNetErrors:
    RECORD_NOT_FOUND = Error('找不到记录', code=Code.NotFound)
    INTERVAL_NOT_REACHED = Error('间隔未到', code=Code.Forbidden)
    LOGIN_FAILED = Error('登录失败', code=Code.Unauthorized)
    LOG_FAILED = Error('获取日志失败', code=Code.InternalServerError)


class RecordValidator:
    MAX_RATE_LENGTH = 10
