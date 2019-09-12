from App.Language.format_syllable import FormatSyllable
from Base.router import Router
from App.Language.character_to_pinyin import CharacterToPinyin

languageRouter = Router()

languageRouter.register('character-to-pinyin', CharacterToPinyin)
languageRouter.register('format-syllable', FormatSyllable)
