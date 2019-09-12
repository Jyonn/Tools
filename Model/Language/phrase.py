from typing import Union, Optional

import pypinyin
from SmartDjango import models, Excp, ErrorCenter, E


class PhraseError(ErrorCenter):
    CREATE_PHRASE = E("新增词语失败")


PhraseError.register()


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

    clen = models.PositiveIntegerField(
        verbose_name='词语长度',
    )

    plen = models.PositiveIntegerField(
        verbose_name='净词语长度',
        help_text='不包含标点符号',
    )
    
    class Meta:
        unique_together = ('cy', 'py')

    @classmethod
    @Excp.pack
    def _create(cls, cy, py, clen, plen):
        cls.validator(locals())

        try:
            phrase = cls(
                cy=cy, py=py, clen=clen, plen=plen,
            )
            phrase.save()
        except Exception:
            return PhraseError.CREATE_PHRASE
        return phrase

    @classmethod
    @Excp.pack
    def create(cls, cy, py: Optional[list] = None):
        if py is None:
            py = pypinyin.pinyin(cy, errors='ignore', style=pypinyin.Style.TONE)
            py = list(map(lambda x: x[0], py))
        clen = len(cy)
        plen = len(py)
        

class Tag(models.Model):
    name = models.CharField(
        verbose_name='标签'
    )


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


class Group(models.Model):
    name = models.CharField(
        verbose_name='组名',
        unique=True,
    )


class GroupSet(models.Model):
    group = models.ForeignKey(
        Group,
        verbose_name='关联组名',
        on_delete=models.CASCADE,
    )


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
