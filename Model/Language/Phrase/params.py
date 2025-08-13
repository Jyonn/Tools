from smartdjango import Params, Validator, ListValidator

from Model.Language.Phrase.models import Phrase, Tag
from Model.Language.Phrase.validators import PhraseValidator


class PhraseParams(metaclass=Params):
    model_class = Phrase

    phrases = ListValidator('phrases').element(Validator().to(Phrase.get_by_id))
    matched = phrases.copy().rename('matched')
    unmatched = phrases.copy().rename('unmatched')

    contributor = Validator('entrance', final_name='contributor').to(PhraseValidator.get_contributor)



class TagParams(metaclass=Params):
    model_class = Tag

    name: Validator
    id_getter = Validator('id', final_name='tag').to(Tag.get_by_id)
