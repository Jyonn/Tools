from Base.router import Router
from Language.character_to_pinyin import CharacterToPinyin

languageRouter = Router()

languageRouter.register('character-to-pinyin', CharacterToPinyin)
