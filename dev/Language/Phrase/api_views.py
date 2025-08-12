import json

from SmartDjango import Analyse, BaseError, P, E
from SmartDjango.models import Pager
from django.views import View
from smartdjango import Error, Code, analyse, Validator, OK

from Base.param_limit import PL
from Model.Base.Config.models import Config
from Model.Language.Phrase.models import Tag, TagMap, Phrase
from Service.Language.phrase import phraseService


PM_TAG_NAME = Tag.get_param('name')
PM_TAG_ID = P('tag_id', yield_name='tag').process(Tag.get_by_id)
PM_PHRASES = P('phrases').validate(list).process(
        lambda phrases: list(map(Phrase.get_by_id, phrases)))
PM_MATCHED = PM_PHRASES.clone().rename('matched')
PM_UNMATCHED = PM_PHRASES.clone().rename('unmatched')
PM_ACTION = P('action').process(str).default('add')


@Error.register
class DevLangPhraseErrors:
    CONTRIBUTOR_NOT_FOUND = Error("贡献者不存在", code=Code.NotFound)


def get_contributor(entrance):
    entrance_key = 'LangPhraseEntrance'
    entrances = json.loads(Config.get_value_by_key(entrance_key))
    if entrance in entrances:
        return entrances[entrance]
    raise DevLangPhraseErrors.CONTRIBUTOR_NOT_FOUND


PM_ENTRANCE = P('entrance', yield_name='contributor').process(get_contributor)


class PhraseView(View):
    @analyse.query(
        PM_TAG_ID,
        Validator('count').to(int).to(PL.number(100, 1))
    )
    def get(self, request):
        tag = request.query.tag
        count = request.query.count

        phrases = phraseService.phrases \
            .exclude(pk__in=TagMap.objects.filter(
                tag=tag, match__isnull=False).values_list('phrase', flat=True)) \
            .order_by('pk')[:count]
        # return phrases.dict(Phrase.d)
        return [phrase.d() for phrase in phrases]

    @analyse.json('cy', PM_ENTRANCE, PM_ACTION, PM_TAG_ID.clone().null())
    def post(self, request):
        cy = request.json.cy
        action = request.json.action

        if action == 'add':
            cy = Phrase.new(cy)
            contributor = request.json.contributor
            add_key = 'LangPhraseAdd-' + contributor
            add_count = int(Config.get_value_by_key(add_key, 0))
            Config.update_value(add_key, str(add_count + 1))
            return cy.d()

        if not request.json.tag:
            return BaseError.MISS_PARAM(('tag_id', '标签'))
        tag = request.json.tag
        cy = Phrase.get(cy)
        tagmap = TagMap.get(cy, tag)
        return tagmap.d()

    @analyse.json(PM_TAG_ID, PM_MATCHED, PM_UNMATCHED, PM_ENTRANCE)
    def put(self, request):
        tag = request.json.tag
        contributor = request.json.contributor

        contributor_key = 'LangPhraseContributor-' + contributor
        contribute_page = int(Config.get_value_by_key(contributor_key, 0))
        Config.update_value(contributor_key, str(contribute_page+1))

        for phrase in request.json.matched():
            TagMap.new_or_put(phrase, tag, match=True)
        for phrase in request.json.unmatched():
            TagMap.new_or_put(phrase, tag, match=False)


class TagView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return [tag.d() for tag in tags]

    @analyse.json(PM_TAG_NAME)
    def post(self, request):
        name = request.json.name
        Tag.new(name)
        return OK

    @analyse.json(PM_TAG_NAME)
    @analyse.query(PM_TAG_ID)
    def put(self, request):
        tag = request.json.tag
        name = request.query.name
        tag.put(name)
        return OK

    @analyse.query(PM_TAG_ID)
    def delete(self, request):
        tag = request.query.tag
        tag.remove()
        return OK


class ContributorView(View):
    @analyse.json(PM_ENTRANCE)
    def post(self, request):
        contributor = request.json.contributor
        contributor_key = 'LangPhraseContributor-' + contributor
        contribute_page = int(Config.get_value_by_key(contributor_key, 0))
        add_key = 'LangPhraseAdd-' + contributor
        add_count = int(Config.get_value_by_key(add_key, 0))

        return dict(contribute_page=contribute_page, add_count=add_count, contributor=contributor)


class ReviewView(View):
    @analyse.query(
        PM_TAG_ID,
        Validator('count').to(int).to(PL.number(100, 1)),
        Validator('last').to(int)
    )
    def get(self, request):
        tag = request.query.tag
        last = request.query.last
        count = request.query.count

        objects = TagMap.objects.search(tag=tag)
        return Pager().page(objects, last, count).dict(TagMap.d)
