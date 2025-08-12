import pypinyin
from smartdjango import Validator, analyse

from Base.handler import BaseHandler
from Base.param_limit import PL


class CharacterToPinyin(BaseHandler):
    APP_NAME = '汉字转拼音'
    APP_DESC = '支持多音字判别，拼音自带音调'

    BODY = [
        Validator('text', '汉字').to(PL.str_len(500)),
        Validator('heteronym_when_single', '单个汉字返回多音字').to(bool).default(True),
    ]
    REQUEST_EXAMPLE = {'text': '林俊杰'}
    RESPONSE_EXAMPLE = ["lín", "jùn", "jié"]

    @staticmethod
    @analyse.json(*BODY)
    def run(r):
        text = r.d.text
        if len(text) == 1:
            pinyin = pypinyin.pinyin(text, heteronym=r.d.heteronym_when_single, errors=lambda _: [None])
            return pinyin[0]

        pinyin = pypinyin.pinyin(text, errors=lambda _: [None])
        return list(map(lambda x: x[0], pinyin))
