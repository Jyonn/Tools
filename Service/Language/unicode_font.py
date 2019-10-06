from typing import List, Optional

from Base.operation import O
from Model.Language.UnicodeFont.models import LetterFont, DigitFont, BaseFont

LNormalBoldItalic = LetterFont('常规-粗斜', '𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁', '𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛').normal().set_bold().set_italic()
LNormal = LetterFont('常规', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz').normal()
LNormalBold = LetterFont('常规-粗', '𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙', '𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳').normal().set_bold()
LNormalItalic = LetterFont('常规-斜', '𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍', '𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝑕𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧').normal().set_italic().unsupport('h')
LFlourish = LetterFont('花体', '𝒜𝒝𝒞𝒟𝒠𝒡𝒢𝒣𝒤𝒥𝒦𝒧𝒨𝒩𝒪𝒫𝒬𝒭𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵', '𝒶𝒷𝒸𝒹𝒺𝒻𝒼𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝓄𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏').flourish().unsupport('BEFHILMRego')
LFlourishBold = LetterFont('花体-粗', '𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩', '𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃').flourish().set_bold()
LOdd = LetterFont('曲折体', '𝔄𝔅𝔆𝔇𝔈𝔉𝔊𝔋𝔌𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔𝔕𝔖𝔗𝔘𝔙𝔚𝔛𝔜𝔝', '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷').odd().unsupport('CHIRZ')
LOddBold = LetterFont('曲折体-粗', '𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅', '𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟').odd().set_bold()
LVoid = LetterFont('空心体', '𝔸𝔹𝔺𝔻𝔼𝔽𝔾𝔿𝕀𝕁𝕂𝕃𝕄𝕅𝕆𝕇𝕈𝕉𝕊𝕋𝕌𝕍𝕎𝕏𝕐𝕑', '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫').void().unsupport('CHNPQRZ')
LTiny = LetterFont('超小体', '𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹', '𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓').tiny()
LTinyBold = LetterFont('超小体-粗', '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭', '𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇').tiny().set_bold()
LTinyItalic = LetterFont('超小体-斜', '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡', '𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻').tiny().set_italic()
LTinyBoldItalic = LetterFont('超小体-粗斜', '𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕', '𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯').tiny().set_bold().set_italic()
LDot = LetterFont('点阵体', '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉', '𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣').dot()
LDouble = LetterFont('全角', 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ', 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ').double()

LetterFonts = [
    LNormalBoldItalic,
    LNormal,
    LNormalBold,
    LNormalItalic,
    LFlourish,
    LFlourishBold,
    LOdd,
    LOddBold,
    LVoid,
    LTiny,
    LTinyBold,
    LTinyItalic,
    LTinyBoldItalic,
    LDot,
    LDouble,
]

DNormalBold = DigitFont('常规-粗', '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗').normal().set_bold()
DNormal = DigitFont('常规', '0123456789').normal()
DVoid = DigitFont('空心体', '𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡').void()
DTiny = DigitFont('超小体', '𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫').tiny()
DTinyBold = DigitFont('超小体-粗', '𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵').tiny().set_bold()
DDot = DigitFont('点阵体', '𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿').dot()
DDouble = DigitFont('全角', '０１２３４５６７８９').double()

DigitFonts = [
    DNormalBold,
    DNormal,
    DVoid,
    DTiny,
    DTinyBold,
    DDot,
    DDouble,
]


class UnicodeFontService:
    def __init__(self):
        self.letter_font_jar = dict()
        self.digit_font_jar = dict()
        self.font_pair = dict()

        self.register(LetterFonts)
        self.register(DigitFonts)
        
        self.auto_prime_setter()
        self.set_prime(LFlourish, DVoid)
        self.set_prime(LFlourishBold, DVoid)
        self.set_prime(LOdd, DVoid)
        self.set_prime(LOddBold, DVoid)

    def register(self, fonts: List[BaseFont]):
        for font in fonts:
            if isinstance(font, LetterFont):
                self.letter_font_jar[font.font_id] = font
            if isinstance(font, DigitFont):
                self.digit_font_jar[font.font_id] = font

    @staticmethod
    def _score(weight, compared):
        if compared:
            return weight
        else:
            return -weight

    def _prime_setter(self, font: BaseFont, candidates: List[BaseFont]):
        best_match = None  # type: BaseFont
        best_score = -1

        for candidate in candidates:
            current_score = 5
            current_score += self._score(5, font.font_type == candidate.font_type)
            current_score += self._score(1, font.bold == candidate.bold)
            current_score += self._score(1, font.italic == candidate.italic)
            if current_score > best_score:
                best_score = current_score
                best_match = candidate

        self.font_pair[font.font_id] = best_match.font_id

    def auto_prime_setter(self):
        for font in LetterFonts:
            self._prime_setter(font, DigitFonts)
        for font in DigitFonts:
            self._prime_setter(font, LetterFonts)

    def set_prime(self, font: BaseFont, prime_font: BaseFont):
        self.font_pair[font.font_id] = prime_font.font_id

    def get_prime(self, font: Optional[BaseFont]):
        if not font:
            return None
        prime_font_id = self.font_pair[font.font_id]
        if isinstance(font, LetterFont):
            return self.digit_font_jar.get(prime_font_id) or DNormalBold
        else:
            return self.letter_font_jar.get(prime_font_id) or LNormalBoldItalic

    @staticmethod
    def purify(sentence: str):
        pure_sentence = ''
        for letter in sentence:
            for font in LetterFonts:
                letter = font.get_pure_letter(letter)
            for font in DigitFonts:
                letter = font.get_pure_letter(letter)
            pure_sentence += letter
        return pure_sentence

    @staticmethod
    def has_letter(pure_sentence):
        for letter in pure_sentence:
            if LNormal.isupper(letter) or LNormal.islower(letter):
                return True
        return False

    @staticmethod
    def has_digit(pure_sentence):
        for digit in pure_sentence:
            if DNormal.isdigit(digit):
                return True
        return False

    def fontify(self,
                sentence: str,
                letter_font: Optional[LetterFont] = None,
                digit_font: Optional[LetterFont] = None,
                purify: bool = True):
        pure_sentence = self.purify(sentence) if purify else sentence
        has_letter = self.has_letter(pure_sentence)
        has_digit = self.has_digit(pure_sentence)

        results = []
        if has_letter:
            letter_fonts = [letter_font] if letter_font else LetterFonts

            for font in letter_fonts:
                supported = font.supporting(pure_sentence)
                sentence = font.translate(pure_sentence)
                results.append(dict(
                    sentence=sentence,
                    letter_font=font,
                    supported=supported
                ))
        else:
            results.append(dict(
                sentence=pure_sentence,
                letter_font=None,
                supported=True,
            ))

        if has_digit:
            if (letter_font or not has_letter) and not digit_font:
                prime_digit_font = digit_font or \
                                   self.get_prime(letter_font) or DigitFonts[0]
                digit_fonts = [digit_font] if digit_font \
                    else O.move_side(DigitFonts, prime_digit_font)
                for index, font in enumerate(digit_fonts):
                    result = results[0].copy()
                    result['digit_font'] = font
                    result['sentence'] = font.translate(result['sentence'])
                    results.append(result)
                results = results[1:]
            else:
                for result in results:
                    prime_digit_font = digit_font or \
                                       self.get_prime(result['letter_font']) or \
                                       DNormalBold
                    result['digit_font'] = prime_digit_font
                    result['sentence'] = prime_digit_font.translate(result['sentence'])

        else:
            for result in results:
                result['digit_font'] = None

        for result in results:
            if result['digit_font']:
                result['digit_font'] = result['digit_font'].d_base()
            if result['letter_font']:
                result['letter_font'] = result['letter_font'].d_base()

        supported_res = []
        unsupported_res = []
        for result in results:
            if result['supported']:
                supported_res.append(result)
            else:
                unsupported_res.append(result)
            del result['supported']

        return dict(
            supported=supported_res,
            unsupported=unsupported_res,
            has_letter=has_letter,
            has_digit=has_digit,
        )


unicodeFontService = UnicodeFontService()
