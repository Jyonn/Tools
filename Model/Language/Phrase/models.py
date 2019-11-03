"""Phrase模型说明
用于存储词语和词语见关联信息

Phrase: 词语表，包含拼音信息
Tag: 标签，如词性（形容词、名词等），情感（喜怒哀乐），是否常用，是否为专业词汇等
Link: 链接，一般用于当某个词可以拆分为另一个词时，两者关系不对等
Group: 分组，如词语翻转/旋转后仍然为另一个词，词之间关系对等
"""
import json
from typing import Optional, List

import pypinyin
from SmartDjango import models, E


@E.register()
class PhraseError:
    SETMEMBER_CONFLICT = E("组内集合元素[{0}]重复")
    GET_GROUPSETMEMBER = E("获取组内集合元素[{0}]失败")
    GROUPSETMEMBER_NOT_FOUND = E("找不到组内集合元素[{0}]")
    CREATE_GROUPSETMEMBER = E("新建组内集合元素[{0}]失败")

    GROUP_NAME_CONFLICT = E("组别[{0}]名称重复")
    CREATE_GROUP = E("新增组别[{0}]失败")
    GET_GROUP = E("获取组别[{0}]失败")
    GROUP_NOT_FOUND = E("找不到组别[{0}]")

    CREATE_LINK = E("新增[{0}]到[{1}]的链接失败")
    GET_LINK = E("获取[{0}]到[{1}]的链接失败")
    LINK_NOT_FOUND = E("找不到[{0}]到[{1}]的链接")

    CREATE_TAGMAP = E("新增[{0}]对应的[{1}]属性失败")
    GET_TAGMAP = E("找到词语[{0}]，获取其[{1}]属性失败")
    TAGMAP_NOT_FOUND = E("找到词语[{0}]，但无[{1}]属性")

    TAG_NAME_CONFLICT = E("属性[{0}]名称重复")
    GET_TAG = E("获取属性[{0}]失败")
    TAG_NOT_FOUND = E("找不到标签[{0}]")
    CREATE_TAG = E("新增属性[{0}]失败")

    PHRASE_NOT_FOUND = E("找不到词语[{0}]")
    GET_PHRASE = E("获取词语[{0}]失败")
    CREATE_PHRASE = E("新增词语[{0}]失败")


class Phrase(models.Model):
    cy = models.CharField(
        verbose_name='词语',
        max_length=20,
        db_index=True,
    )

    py = models.CharField(
        verbose_name='拼音',
        max_length=150,
    )

    number_py = models.CharField(
        verbose_name='带数字带拼音',
        max_length=165,
        default=None
    )

    clen = models.PositiveIntegerField(
        verbose_name='词语长度',
    )

    plen = models.PositiveIntegerField(
        verbose_name='净词语长度',
        help_text='不包含标点符号',
    )

    class Meta:
        unique_together = ('cy', 'number_py')

    def __str__(self):
        return self.cy + ' ' + ' '.join(json.loads(self.py))

    @staticmethod
    def get_number_py(py: List):
        number_py = []
        for py_ in py:
            from Service.Language.phrase import phraseService
            number_py.append(phraseService.format_syllable(py_, printer='number_toner'))
        number_py = json.dumps(number_py, ensure_ascii=False)
        return number_py

    @classmethod
    def _get(cls, cy, number_py):
        cls.validator(locals())

        try:
            return cls.objects.get(cy=cy, number_py=number_py)
        except cls.DoesNotExist:
            raise PhraseError.PHRASE_NOT_FOUND(cy)
        except Exception as err:
            raise PhraseError.GET_PHRASE(cy, debug_message=err)

    @classmethod
    def get(cls, cy, py: Optional[list] = None):
        if py is None:
            py = pypinyin.pinyin(cy, errors='ignore', style=pypinyin.Style.TONE)
            py = list(map(lambda x: x[0], py))
        number_py = cls.get_number_py(py)
        return cls._get(cy, number_py)

    @classmethod
    def get_by_id(cls, id_):
        try:
            return cls.objects.get(pk=id_)
        except cls.DoesNotExist:
            raise PhraseError.PHRASE_NOT_FOUND(id_)
        except Exception as err: 
            raise PhraseError.GET_PHRASE(id_, debug_message=err)

    @classmethod
    def _new(cls, cy, py, clen, plen, number_py):
        cls.validator(locals())

        try:
            phrase = cls(cy=cy, py=py, clen=clen, plen=plen, number_py=number_py)
            phrase.save()
        except Exception as err:
            raise PhraseError.CREATE_PHRASE(cy, debug_message=err)
        return phrase

    @classmethod
    def new(cls, cy, py: Optional[list] = None):
        if py is None:
            py = pypinyin.pinyin(cy, errors='ignore', style=pypinyin.Style.TONE)
            py = list(map(lambda x: x[0], py))
        clen = len(cy)
        plen = len(py)

        number_py = cls.get_number_py(py)

        py = json.dumps(py, ensure_ascii=False)
        return cls._new(cy, py, clen, plen, number_py)

    def _readable_id(self):
        return self.pk

    def _readable_py(self):
        return json.loads(self.py)

    def d(self):
        return self.dictor('cy', 'py', 'id')


class Tag(models.Model):
    name = models.CharField(
        verbose_name='标签',
        max_length=10,
        unique=True,
    )

    start = models.IntegerField(
        verbose_name='标注进展',
        default=0,
    )

    @classmethod
    def get_by_id(cls, id_):
        try:
            return cls.objects.get(pk=id_)
        except cls.DoesNotExist:
            raise PhraseError.TAG_NOT_FOUND(id_)
        except Exception as err:
            raise PhraseError.GET_TAG(id_, debug_message=err)

    @classmethod
    def get(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise PhraseError.TAG_NOT_FOUND(name)
        except Exception as err:
            raise PhraseError.GET_TAG(name, debug_message=err)

    @classmethod
    def new(cls, name):
        try:
            cls.get(name)
        except E as e:
            if e.eis(PhraseError.TAG_NOT_FOUND):
                try:
                    tag = cls(name=name, start=0)
                    tag.save()
                except Exception as err:
                    raise PhraseError.CREATE_TAG(name, debug_message=err)
                return tag
            else:
                return e
        raise PhraseError.TAG_NAME_CONFLICT

    def put(self, name):
        self.name = name
        self.save()

    def remove(self):
        self.delete()

    def _readable_id(self):
        return self.pk

    def d(self):
        return self.dictor('name', 'start', 'id')


class TagMap(models.Model):
    phrase = models.ForeignKey(
        Phrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        Tag,
        verbose_name='关联标签',
        on_delete=models.CASCADE,
    )

    match = models.NullBooleanField(
        verbose_name='是否匹配',
        help_text='null未知 true匹配 false相反'
    )

    class Meta:
        unique_together = ('phrase', 'tag')

    @classmethod
    def get(cls, phrase: Phrase, tag: Tag):
        try:
            return cls.objects.get(phrase=phrase, tag=tag)
        except cls.DoesNotExist:
            raise PhraseError.TAGMAP_NOT_FOUND(phrase.cy, tag.name)
        except Exception as err:
            raise PhraseError.GET_TAGMAP(phrase.cy, tag.name, debug_message=err)

    @classmethod
    def new_or_put(cls, phrase, tag, match=True):
        try:
            tagmap = cls.get(phrase, tag)
            tagmap.match = match
            tagmap.save()
        except E as e:
            if e.eis(PhraseError.TAGMAP_NOT_FOUND):
                try:
                    tagmap = cls(
                        phrase=phrase,
                        tag=tag,
                        match=match,
                    )
                    tagmap.save()
                except Exception as err: 
                    raise PhraseError.CREATE_TAGMAP(phrase.cy, tag.name, debug_message=err)
            else:
                return e
        return tagmap

    def _readable_phrase(self):
        return self.phrase.d()

    def d(self):
        return self.dictor('phrase', 'match')


class Link(models.Model):
    linking = models.ForeignKey(
        Phrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
        related_name='linking',
    )

    linked = models.ForeignKey(
        Phrase,
        verbose_name='被关联词语',
        on_delete=models.CASCADE,
        related_name='linked',
    )

    class Meta:
        unique_together = ('linking', 'linked')

    @classmethod
    def get(cls, linking: Phrase, linked: Phrase):
        try:
            return cls.objects.get(linked=linked, linking=linking)
        except cls.DoesNotExist:
            raise PhraseError.LINK_NOT_FOUND(linking.cy, linked.cy)
        except Exception as err: 
            raise PhraseError.GET_LINK(linking.cy, linked.cy, debug_message=err)

    @classmethod
    def new_or_get(cls, linking: Phrase, linked: Phrase):
        try:
            link = cls.get(linking, linked)
        except E as ret:
            if ret.eis(PhraseError.LINK_NOT_FOUND):
                try:
                    link = cls(
                        linking=linking,
                        linked=linked,
                    )
                    link.save()
                except Exception as err: 
                    raise PhraseError.CREATE_LINK(linking.cy, linked.cy, debug_message=err)
            else:
                raise ret
        return link


class Group(models.Model):
    name = models.CharField(
        verbose_name='组名',
        unique=True,
        max_length=10,
    )

    @classmethod
    def get(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise PhraseError.GROUP_NOT_FOUND(name)
        except Exception as err: 
            raise PhraseError.GET_GROUP(name, debug_message=err)

    @classmethod
    def new(cls, name):
        try:
            cls.get(name)
        except E as e:
            if e.eis(PhraseError.GROUP_NOT_FOUND):
                try:
                    group = cls(name=name)
                    group.save()
                except Exception as err: 
                    raise PhraseError.CREATE_GROUP(name, debug_message=err)
            else:
                return e
        raise PhraseError.GROUP_NAME_CONFLICT

    def push(self, phrases: List[Phrase]):
        return GroupSet.new(self, phrases)


class GroupSet(models.Model):
    group = models.ForeignKey(
        Group,
        verbose_name='关联组名',
        on_delete=models.CASCADE,
    )

    @classmethod
    def new(cls, group, phrases: List[Phrase]):
        set_ = cls(group=group)
        set_.save()
        for phrase in phrases:
            GroupSetMember.new(set_, phrase)
        return set_


class GroupSetMember(models.Model):
    set = models.ForeignKey(
        GroupSet,
        verbose_name='集合',
        on_delete=models.CASCADE,
    )

    phrase = models.ForeignKey(
        Phrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('set', 'phrase')

    @classmethod
    def get(cls, set_: GroupSet, phrase: Phrase):
        try:
            return cls.objects.get(set=set_, phrase=phrase)
        except cls.DoesNotExist:
            raise PhraseError.GROUPSETMEMBER_NOT_FOUND(phrase.cy)
        except Exception as err: 
            raise PhraseError.GET_GROUPSETMEMBER(phrase.cy, debug_message=err)

    @classmethod
    def new(cls, set_: GroupSet, phrase: Phrase):
        try:
            cls.get(set_, phrase)
        except E as ret:
            if ret.eis(PhraseError.GROUPSETMEMBER_NOT_FOUND):
                try:
                    member = cls(set=set_, phrase=phrase)
                    member.save()
                    return member
                except Exception as err: 
                    raise PhraseError.CREATE_GROUPSETMEMBER(phrase.cy, debug_message=err)
            else:
                return ret
        raise PhraseError.SETMEMBER_CONFLICT(phrase.cy)
