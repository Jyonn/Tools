import json

from smartdjango import Error, Code, Validator

from Model.Base.Config.models import Config


@Error.register
class PhraseErrors:
    SETMEMBER_CONFLICT = Error("组内集合元素[{name}]重复", code=Code.BadRequest)
    GET_GROUPSETMEMBER = Error("获取组内集合元素[{name}]失败", code=Code.InternalServerError)
    GROUPSETMEMBER_NOT_FOUND = Error("找不到组内集合元素[{name}]", code=Code.NotFound)
    CREATE_GROUPSETMEMBER = Error("新建组内集合元素[{name}]失败", code=Code.InternalServerError)

    GROUP_NAME_CONFLICT = Error("组别[{name}]名称重复", code=Code.BadRequest)
    CREATE_GROUP = Error("新增组别[{name}]失败", code=Code.InternalServerError)
    GET_GROUP = Error("获取组别[{name}]失败", code=Code.InternalServerError)
    GROUP_NOT_FOUND = Error("找不到组别[{name}]", code=Code.NotFound)

    CREATE_LINK = Error("新增[{source}]到[{target}]的链接失败", code=Code.InternalServerError)
    GET_LINK = Error("获取[{source}]到[{target}]的链接失败", code=Code.InternalServerError)
    LINK_NOT_FOUND = Error("找不到[{source}]到[{target}]的链接", code=Code.NotFound)

    CREATE_TAGMAP = Error("新增[{name}]对应的[{attr}]属性失败", code=Code.InternalServerError)
    GET_TAGMAP = Error("找到词语[{name}]，获取其[{attr}]属性失败", code=Code.InternalServerError)
    TAGMAP_NOT_FOUND = Error("找到词语[{name}]，但无[{attr}]属性", code=Code.NotFound)

    TAG_NAME_CONFLICT = Error("属性[{name}]名称重复", code=Code.BadRequest)
    GET_TAG = Error("获取属性[{name}]失败", code=Code.InternalServerError)
    TAG_NOT_FOUND = Error("找不到标签[{name}]", code=Code.NotFound)
    CREATE_TAG = Error("新增属性[{name}]失败", code=Code.InternalServerError)

    PHRASE_NOT_FOUND = Error("找不到词语[{name}]", code=Code.NotFound)
    GET_PHRASE = Error("获取词语[{name}]失败", code=Code.InternalServerError)
    CREATE_PHRASE = Error("新增词语[{name}]失败", code=Code.InternalServerError)

    TAG_MISS = Error("缺少标签参数", code=Code.BadRequest)

    CONTRIBUTOR_NOT_FOUND = Error("贡献者不存在", code=Code.NotFound)


class PhraseValidator:
    MAX_CY_LENGTH = 20
    MAX_PY_LENGTH = 150
    MAX_NUMBER_PY_LENGTH = 165

    @classmethod
    def get_contributor(cls, entrance):
        entrance_key = 'LangPhraseEntrance'
        entrances = json.loads(Config.get_value_by_key(entrance_key))
        if entrance in entrances:
            return entrances[entrance]
        raise PhraseErrors.CONTRIBUTOR_NOT_FOUND
