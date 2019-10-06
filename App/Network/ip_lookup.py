from SmartDjango import Analyse, P

from Base.handler import BaseHandler
from Base.param_limit import PL
from Model.Network.IP.models import IP


class IPLookup(BaseHandler):
    APP_NAME = '国内IP查询'
    APP_DESC = '获取地域和IP段'

    BODY = [P('ip', 'ip地址').process(PL.ip_dot2int).process(IP.lookup)]

    REQUEST_EXAMPLE = {"ip": "39.174.135.244"}
    RESPONSE_EXAMPLE = {
        "city": "杭州",
        "line": "移动",
        "province": "浙江省",
        "ip_start": "39.174.128.0",
        "ip_end": "39.174.255.255",
        "owner": "",
        "country": "中国"
    }

    @staticmethod
    @Analyse.r(b=BODY)
    def run(r):
        return r.d.ip.d()
