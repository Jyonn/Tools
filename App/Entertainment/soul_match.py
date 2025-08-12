"""
关闭入口@200425
"""

import requests
from smartdjango import Validator, analyse

from Base.handler import BaseHandler


class SoulMatch(BaseHandler):
    APP_NAME = '朋友圈默契度偷窥'
    APP_DESC = '2020朋友圈默契大考验偷窥工具'

    BODY = [Validator('openid', '微信用户ID')]

    @staticmethod
    @analyse.json(*BODY)
    def run(request):
        openid = request.json.openid
        data = requests.get('https://2020luck.news.qq.com/friend/getInfo?openId='+openid).json()
        return data['data']
