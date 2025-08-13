import json

from smartdjango import Error, Code, Validator

from Model.Base.Config.models import Config


@Error.register
class PhraseErrors:
    SETMEMBER_CONFLICT = Error("组内集合元素[{0}]重复", code=Code.BadRequest)
    GET_GROUPSETMEMBER = Error("获取组内集合元素[{0}]失败", code=Code.InternalServerError)
    GROUPSETMEMBER_NOT_FOUND = Error("找不到组内集合元素[{0}]", code=Code.NotFound)
    CREATE_GROUPSETMEMBER = Error("新建组内集合元素[{0}]失败", code=Code.InternalServerError)

    GROUP_NAME_CONFLICT = Error("组别[{0}]名称重复", code=Code.BadRequest)
    CREATE_GROUP = Error("新增组别[{0}]失败", code=Code.InternalServerError)
    GET_GROUP = Error("获取组别[{0}]失败", code=Code.InternalServerError)
    GROUP_NOT_FOUND = Error("找不到组别[{0}]", code=Code.NotFound)

    CREATE_LINK = Error("新增[{0}]到[{1}]的链接失败", code=Code.InternalServerError)
    GET_LINK = Error("获取[{0}]到[{1}]的链接失败", code=Code.InternalServerError)
    LINK_NOT_FOUND = Error("找不到[{0}]到[{1}]的链接", code=Code.NotFound)

    CREATE_TAGMAP = Error("新增[{0}]对应的[{1}]属性失败", code=Code.InternalServerError)
    GET_TAGMAP = Error("找到词语[{0}]，获取其[{1}]属性失败", code=Code.InternalServerError)
    TAGMAP_NOT_FOUND = Error("找到词语[{0}]，但无[{1}]属性", code=Code.NotFound)

    TAG_NAME_CONFLICT = Error("属性[{0}]名称重复", code=Code.BadRequest)
    GET_TAG = Error("获取属性[{0}]失败", code=Code.InternalServerError)
    TAG_NOT_FOUND = Error("找不到标签[{0}]", code=Code.NotFound)
    CREATE_TAG = Error("新增属性[{0}]失败", code=Code.InternalServerError)

    PHRASE_NOT_FOUND = Error("找不到词语[{0}]", code=Code.NotFound)
    GET_PHRASE = Error("获取词语[{0}]失败", code=Code.InternalServerError)
    CREATE_PHRASE = Error("新增词语[{0}]失败", code=Code.InternalServerError)

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
