from SmartDjango import Excp, Analyse, Param
from django.views import View

from Base.param_limit import PL
from Model.Language.Phrase.models import Tag, TagMap, Phrase
from Service.Language.phrase import phraseService


PM_TAG_NAME = Tag.get_param('name')
PM_TAG_ID = Param('tag_id').process(Param.Processor(Tag.get_by_id, yield_name='tag'))
PM_PHRASES = Param('phrases').validate(list).process(
        lambda phrases: list(map(Phrase.get_by_id, phrases)))
PM_MATCHED = PM_PHRASES.clone().rename('matched')
PM_UNMATCHED = PM_PHRASES.clone().rename('unmatched')


class PhraseView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(q=[PM_TAG_ID, Param('count').process(int).process(PL.number(100, 1))])
    def get(r):
        tag = r.d.tag
        count = r.d.count

        phrases = phraseService.phrases \
            .exclude(pk__in=TagMap.objects.filter(
                tag=tag, match__isnull=False).values_list('phrase', flat=True)) \
            .order_by('pk')[:count]
        return phrases.dict(Phrase.d)

    @staticmethod
    @Excp.handle
    @Analyse.r(b=[PM_TAG_ID, PM_MATCHED, PM_UNMATCHED])
    def put(r):
        tag = r.d.tag
        for phrase in r.d.matched:
            TagMap.new_or_put(phrase, tag, match=True)
        for phrase in r.d.unmatched:
            TagMap.new_or_put(phrase, tag, match=False)


class TagView(View):
    @staticmethod
    @Excp.handle
    def get(r):
        return Tag.objects.dict(Tag.d)

    @staticmethod
    @Excp.handle
    @Analyse.r(b=[PM_TAG_NAME])
    def post(r):
        name = r.d.name
        Tag.new(name)

    @staticmethod
    @Excp.handle
    @Analyse.r(b=[PM_TAG_NAME], q=[PM_TAG_ID])
    def put(r):
        tag = r.d.tag
        name = r.d.name
        # tag.
        tag.put(name)

    @staticmethod
    @Excp.handle
    @Analyse.r(q=[PM_TAG_ID])
    def delete(r):
        tag = r.d.tag
        tag.remove()

