from django.views import View
from smartdjango import analyse, Validator, OK

from Base.param_limit import PL
from Model.Base.Config.models import Config
from Model.Language.Phrase.models import Tag, TagMap, Phrase
from Model.Language.Phrase.params import TagParams, PhraseParams
from Model.Language.Phrase.validators import PhraseErrors
from Service.Language.phrase import phraseService


class PhraseView(View):
    @analyse.query(
        TagParams.id_getter,
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

    @analyse.json(
        'cy',
        PhraseParams.contributor,
        Validator('action').to(str).default('add'),
        TagParams.id_getter.clone().null()
    )
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
            return PhraseErrors.TAG_MISS
        tag = request.json.tag
        cy = Phrase.get(cy)
        tagmap = TagMap.get(cy, tag)
        return tagmap.d()

    @analyse.json(
        TagParams.id_getter,
        PhraseParams.matched,
        PhraseParams.unmatched,
        PhraseParams.contributor
    )
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

    @analyse.json(TagParams.name)
    def post(self, request):
        name = request.json.name
        Tag.new(name)
        return OK

    @analyse.json(TagParams.name)
    @analyse.query(TagParams.id_getter)
    def put(self, request):
        tag = request.json.tag
        name = request.query.name
        tag.put(name)
        return OK

    @analyse.query(TagParams.id_getter)
    def delete(self, request):
        tag = request.query.tag
        tag.remove()
        return OK


class ContributorView(View):
    @analyse.json(PhraseParams.contributor)
    def post(self, request):
        contributor = request.json.contributor
        contributor_key = 'LangPhraseContributor-' + contributor
        contribute_page = int(Config.get_value_by_key(contributor_key, 0))
        add_key = 'LangPhraseAdd-' + contributor
        add_count = int(Config.get_value_by_key(add_key, 0))

        return dict(contribute_page=contribute_page, add_count=add_count, contributor=contributor)


class ReviewView(View):
    @analyse.query(
        TagParams.id_getter,
        Validator('count').to(int).to(PL.number(100, 1)),
        Validator('last').to(int)
    )
    def get(self, request):
        tag = request.query.tag
        last = request.query.last
        count = request.query.count

        tagmaps = TagMap.objects.filter(tag=tag, pk__gt=last).order_by('pk')[:count]
        return [tagmap.d() for tagmap in tagmaps]
