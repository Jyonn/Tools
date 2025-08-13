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
from diq import Dictify
from django.db import models
from smartdjango import Error

from Model.Language.Phrase.validators import PhraseValidator, PhraseErrors


class Phrase(models.Model, Dictify):
    vldt = PhraseValidator

    cy = models.CharField(
        verbose_name='词语',
        max_length=vldt.MAX_CY_LENGTH,
        db_index=True,
    )

    py = models.CharField(
        verbose_name='拼音',
        max_length=vldt.MAX_PY_LENGTH,
    )

    number_py = models.CharField(
        verbose_name='带数字带拼音',
        max_length=vldt.MAX_NUMBER_PY_LENGTH,
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
        # cls.validator(locals())
        # TODO: validator

        try:
            return cls.objects.get(cy=cy, number_py=number_py)
        except cls.DoesNotExist:
            raise PhraseErrors.PHRASE_NOT_FOUND(name=cy)
        except Exception as err:
            raise PhraseErrors.GET_PHRASE(name=cy, details=err)

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
            raise PhraseErrors.PHRASE_NOT_FOUND(name=id_)
        except Exception as err: 
            raise PhraseErrors.GET_PHRASE(name=id_, details=err)

    @classmethod
    def _new(cls, cy, py, clen, plen, number_py):
        # cls.validator(locals())
        # TODO: validator

        try:
            phrase = cls(cy=cy, py=py, clen=clen, plen=plen, number_py=number_py)
            phrase.save()
        except Exception as err:
            raise PhraseErrors.CREATE_PHRASE(name=cy, details=err)
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
        return self.dictify('cy', 'py', 'id')


class Tag(models.Model, Dictify):
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
            raise PhraseErrors.TAG_NOT_FOUND(name=id_)
        except Exception as err:
            raise PhraseErrors.GET_TAG(name=id_, details=err)

    @classmethod
    def get(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            raise PhraseErrors.TAG_NOT_FOUND(name=name)
        except Exception as err:
            raise PhraseErrors.GET_TAG(name=name, details=err)

    @classmethod
    def new(cls, name):
        try:
            cls.get(name)
        except Error as e:
            if e == PhraseErrors.TAG_NOT_FOUND:
                try:
                    tag = cls(name=name, start=0)
                    tag.save()
                except Exception as err:
                    raise PhraseErrors.CREATE_TAG(name=name, details=err)
                return tag
            else:
                return e
        raise PhraseErrors.TAG_NAME_CONFLICT(name=name)

    def put(self, name):
        self.name = name
        self.save()

    def remove(self):
        self.delete()

    def _readable_id(self):
        return self.pk

    def d(self):
        return self.dictify('name', 'start', 'id')


class TagMap(models.Model, Dictify):
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

    match = models.BooleanField(
        verbose_name='是否匹配',
        help_text='null未知 true匹配 false相反',
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('phrase', 'tag')

    @classmethod
    def get(cls, phrase: Phrase, tag: Tag):
        try:
            return cls.objects.get(phrase=phrase, tag=tag)
        except cls.DoesNotExist:
            raise PhraseErrors.TAGMAP_NOT_FOUND(name=phrase.cy, attr=tag.name)
        except Exception as err:
            raise PhraseErrors.GET_TAGMAP(name=phrase.cy, attr=tag.name, details=err)

    @classmethod
    def new_or_put(cls, phrase, tag, match=True):
        try:
            tagmap = cls.get(phrase, tag)
            tagmap.match = match
            tagmap.save()
        except Error as e:
            if e == PhraseErrors.TAGMAP_NOT_FOUND:
                try:
                    tagmap = cls(
                        phrase=phrase,
                        tag=tag,
                        match=match,
                    )
                    tagmap.save()
                except Exception as err: 
                    raise PhraseErrors.CREATE_TAGMAP(name=phrase.cy, attr=tag.name, details=err)
            else:
                return e
        return tagmap

    def _readable_phrase(self):
        return self.phrase.d()

    def d(self):
        return self.dictify('phrase', 'match')


class Link(models.Model, Dictify):
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
            raise PhraseErrors.LINK_NOT_FOUND(source=linking.cy, target=linked.cy)
        except Exception as err: 
            raise PhraseErrors.GET_LINK(source=linking.cy, target=linked.cy, details=err)

    @classmethod
    def new_or_get(cls, linking: Phrase, linked: Phrase):
        try:
            link = cls.get(linking, linked)
        except Error as e:
            if e == PhraseErrors.LINK_NOT_FOUND:
                try:
                    link = cls(
                        linking=linking,
                        linked=linked,
                    )
                    link.save()
                except Exception as err: 
                    raise PhraseErrors.CREATE_LINK(source=linking.cy, target=linked.cy, details=err)
            else:
                raise e
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
            raise PhraseErrors.GROUP_NOT_FOUND(name=name)
        except Exception as err: 
            raise PhraseErrors.GET_GROUP(name=name, details=err)

    @classmethod
    def new(cls, name):
        try:
            cls.get(name)
        except Error as e:
            if e == PhraseErrors.GROUP_NOT_FOUND:
                try:
                    group = cls(name=name)
                    group.save()
                except Exception as err: 
                    raise PhraseErrors.CREATE_GROUP(name=name, details=err)
            else:
                return e
        raise PhraseErrors.GROUP_NAME_CONFLICT(name=name)

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
            raise PhraseErrors.GROUPSETMEMBER_NOT_FOUND(name=phrase.cy)
        except Exception as err: 
            raise PhraseErrors.GET_GROUPSETMEMBER(name=phrase.cy, details=err)

    @classmethod
    def new(cls, set_: GroupSet, phrase: Phrase):
        try:
            cls.get(set_, phrase)
        except Error as e:
            if e == PhraseErrors.GROUPSETMEMBER_NOT_FOUND:
                try:
                    member = cls(set=set_, phrase=phrase)
                    member.save()
                    return member
                except Exception as err: 
                    raise PhraseErrors.CREATE_GROUPSETMEMBER(name=phrase.cy, details=err)
            else:
                return e
        raise PhraseErrors.SETMEMBER_CONFLICT(name=phrase.cy)
