from SmartDjango import Excp, Analyse, Param, BaseError
from SmartDjango.models import Pager
from django.views import View

from Base.param_limit import PL
from Model.Base.Config.models import Config
from Model.Language.Phrase.models import Tag, TagMap, Phrase
from Service.Language.phrase import phraseService


PM_TAG_NAME = Tag.get_param('name')
PM_TAG_ID = Param('tag_id').process(Param.Processor(Tag.get_by_id, yield_name='tag'))
PM_PHRASES = Param('phrases').validate(list).process(
        lambda phrases: list(map(Phrase.get_by_id, phrases)))
PM_MATCHED = PM_PHRASES.clone().rename('matched')
PM_UNMATCHED = PM_PHRASES.clone().rename('unmatched')
PM_CONTRIBUTOR = Param('contributor').process(str).set_default('')
PM_ACTION = Param('action').process(str).set_default('add')


class PhraseView(View):
    @staticmethod
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
    @Analyse.r(b=['cy', PM_CONTRIBUTOR, PM_ACTION, PM_TAG_ID.clone().set_null()])
    def post(r):
        cy = r.d.cy
        action = r.d.action

        if action == 'add':
            cy = Phrase.new(cy)
            contributor = r.d.contributor
            add_key = 'LangPhraseAdd-' + contributor
            add_count = int(Config.get_value_by_key(add_key, 0))
            Config.update_value(add_key, str(add_count + 1))
            return cy.d()
        else:
            if not r.d.tag:
                return BaseError.MISS_PARAM(('tag_id', '标签'))
            tag = r.d.tag
            cy = Phrase.get(cy)
            tagmap = TagMap.get(cy, tag)
            return tagmap.d()

    @staticmethod
    @Analyse.r(b=[PM_TAG_ID, PM_MATCHED, PM_UNMATCHED, PM_CONTRIBUTOR])
    def put(r):
        tag = r.d.tag
        contributor = r.d.contributor

        contributor_key = 'LangPhraseContributor-'+contributor
        contribute_page = int(Config.get_value_by_key(contributor_key, 0))
        Config.update_value(contributor_key, str(contribute_page+1))

        for phrase in r.d.matched:
            TagMap.new_or_put(phrase, tag, match=True)
        for phrase in r.d.unmatched:
            TagMap.new_or_put(phrase, tag, match=False)


class TagView(View):
    @staticmethod
    def get(r):
        return Tag.objects.dict(Tag.d)

    @staticmethod
    @Analyse.r(b=[PM_TAG_NAME])
    def post(r):
        name = r.d.name
        Tag.new(name)

    @staticmethod
    @Analyse.r(b=[PM_TAG_NAME], q=[PM_TAG_ID])
    def put(r):
        tag = r.d.tag
        name = r.d.name
        tag.put(name)

    @staticmethod
    @Analyse.r(q=[PM_TAG_ID])
    def delete(r):
        tag = r.d.tag
        tag.remove()


class ContributorView(View):
    @staticmethod
    @Excp.handle
    @Analyse.r(b=[PM_CONTRIBUTOR])
    def post(r):
        contributor = r.d.contributor
        contributor_key = 'LangPhraseContributor-' + contributor
        contribute_page = int(Config.get_value_by_key(contributor_key, 0))
        add_key = 'LangPhraseAdd-' + contributor
        add_count = int(Config.get_value_by_key(add_key, 0))

        return dict(contribute_page=contribute_page, add_count=add_count)


class ReviewView(View):
    @staticmethod
    @Analyse.r(q=[
        PM_TAG_ID,
        Param('count').process(int).process(PL.number(100, 1)),
        Param('last').process(int)
    ])
    def get(r):
        tag = r.d.tag
        last = r.d.last
        count = r.d.count

        objects = TagMap.objects.search(tag=tag)
        return Pager().page(objects, last, count).dict(TagMap.d)
