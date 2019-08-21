import pypinyin
from SmartDjango import Packing, Param, Analyse

from Base.handler import BaseHandler
from Base.param_limit import PL


class CharacterToPinyin(BaseHandler):
    APP_NAME = '汉字转拼音'
    APP_DESC = '支持多音字判别，拼音自带音调'

    QUERY = [Param('text', '汉字').validate(PL.str_len(500))]

    @staticmethod
    @Packing.http_pack
    @Analyse.r(q=QUERY)
    def run(r):
        text = r.d.text
        pinyin = pypinyin.pinyin(text, errors=lambda _: [None])
        return list(map(lambda x: x[0], pinyin))
