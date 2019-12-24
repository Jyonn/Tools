import requests
from SmartDjango import P, Analyse

from Base.handler import BaseHandler


class SoulMatch(BaseHandler):
    APP_NAME = '朋友圈默契度偷窥'
    APP_DESC = '2020朋友圈默契大考验偷窥工具'

    BODY = [P('openid', '微信用户ID')]

    @staticmethod
    @Analyse.r(b=BODY)
    def run(r):
        openid = r.d.openid
        data = requests.get('https://2020luck.news.qq.com/friend/getInfo?openId='+openid).json()
        return data['data']
