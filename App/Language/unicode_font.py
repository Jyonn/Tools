from SmartDjango import Analyse, P, Processor

from Base.handler import BaseHandler
from Base.router import Router
from Service.Language.unicode_font import unicodeFontService, LetterFonts, DigitFonts


class UnicodeFont(BaseHandler):
    class FontHandler(BaseHandler):
        APP_NAME = '英文和数字字体列表'
        APP_DESC = 'digit_font_id和letter_font_id的取值说明。\n' \
                   '通过POST请求获取所有字体列表。\n' \
                   'digit_font_id和letter_font_id的值只需传入id即可。'

        @staticmethod
        def run(r):
            return dict(
                letter_fonts=list(map(lambda font: font.d(), LetterFonts)),
                digit_fonts=list(map(lambda font: font.d(), DigitFonts)),
            )

    class PurifyHandler(BaseHandler):
        APP_NAME = '字体清洁'
        APP_DESC = 'purify的取值说明。\n' \
                   '当sentence中存在已改变字体的字符时，若purify取true表示将这些字体还原为原始字符，' \
                   '随着letter_font_id和digit_font_id所代表的字体变动；\n' \
                   '若purify取false表示这部分字符不随letter_font_id和digit_font_id所代表的字体变动。'

    APP_NAME = '英文变字体'
    APP_DESC = '将正常的英文变为粗体、斜体、花体等，支持微博、朋友圈等常见APP'

    BODY = [
        P('sentence', '句子').validate(str),
        P('letter_font_id', '英文字体ID')
            .process(Processor(unicodeFontService.letter_font_jar.get, yield_name='letter_font'))
            .null(),
        P('digit_font_id', '数字字体ID')
            .process(Processor(unicodeFontService.digit_font_jar.get, yield_name='digit_font'))
            .null(),
        P('purify', '是否进行字体清洁').validate(bool).default(True),
    ]

    REQUEST_EXAMPLE = {
        "sentence": "Emma is Jyonn's apple.",
        "letter_font_id": 8,
        "purify": True
    }
    RESPONSE_EXAMPLE = {
        "supported": [
            {
                "sentence": "𝔼𝕞𝕞𝕒 𝕚𝕤 𝕁𝕪𝕠𝕟𝕟'𝕤 𝕒𝕡𝕡𝕝𝕖.",
                "letter_font": {
                    "font_name": "空心体",
                    "font_id": 8
                },
                "digit_font": None
            }
        ],
        "unsupported": [],
        "has_letter": True,
        "has_digit": False,
    }

    SUB_ROUTER = Router()
    SUB_ROUTER.register_usage('font', FontHandler)
    SUB_ROUTER.register_usage('purify', PurifyHandler)

    @staticmethod
    @Analyse.r(b=BODY)
    def run(r):
        sentence = r.d.sentence
        letter_font = r.d.letter_font
        digit_font = r.d.digit_font
        purity = r.d.purify

        return unicodeFontService.fontify(sentence, letter_font, digit_font, purity)
