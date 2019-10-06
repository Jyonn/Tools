from App.Language.character_to_pinyin import CharacterToPinyin
from App.Language.format_syllable import FormatSyllable
from App.Language.rythme import Rythme
from App.Language.unicode_font import UnicodeFont
from Base.router import Router

languageRouter = Router()

languageRouter.register('character-to-pinyin', CharacterToPinyin)
languageRouter.register('format-syllable', FormatSyllable)
languageRouter.register('rythme', Rythme)
languageRouter.register('unicode-font', UnicodeFont)
