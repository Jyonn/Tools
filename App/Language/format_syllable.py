from smartdjango import Validator, analyse

from Base.handler import BaseHandler
from Service.Language.phrase import phraseService


class FormatSyllable(BaseHandler):
    APP_NAME = '格式化音节'
    APP_DESC = '将带数字的不标准音节格式化为标准带声调音节'

    BODY = [Validator('syllables', '音节列表').to(list)]

    REQUEST_EXAMPLE = {"syllables": ["hua", "fe3ng", "lv2", "shān"]}
    RESPONSE_EXAMPLE = ["hua", "fěng", "lǘ", "shān"]

    @staticmethod
    @analyse.json(*BODY)
    def run(request):
        syllables = request.json.syllables  # type: list
        return list(map(phraseService.format_syllable, syllables))
