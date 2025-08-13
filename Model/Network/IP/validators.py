from smartdjango import Error, Code


@Error.register
class IPErrors:
    IP_NOT_FOUND = Error("找不到IP[{ip}]", code=Code.NotFound)
    CREATE_IP = Error("增加IP[{ip}]失败", code=Code.InternalServerError)
    GET_IP = Error("查找IP[{ip}]失败", Code.InternalServerError)



class IPValidator:
    MAX_COUNTRY_LENGTH = 10
    MAX_PROVINCE_LENGTH = 10
    MAX_CITY_LENGTH = 20
    MAX_OWNER_LENGTH = 40
    MAX_LINE_LENGTH = 30
