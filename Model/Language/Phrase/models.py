from typing import Optional

import pypinyin
from SmartDjango import models, Excp, ErrorCenter, E


class PhraseError(ErrorCenter):
    CREATE_PHRASE = E("新增词语失败")


PhraseError.register()


class LangPhrPhrase(models.Model):
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


class LangPhrTag(models.Model):
    name = models.CharField(
        verbose_name='标签'
    )


class LangPhrTagMap(models.Model):
    phrase = models.ForeignKey(
        LangPhrPhrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        LangPhrTag,
        verbose_name='关联标签',
        on_delete=models.CASCADE,
    )

    match = models.NullBooleanField(
        verbose_name='是否匹配',
        help_text='null未知 true匹配 false相反'
    )

    class Meta:
        unique_together = ('phrase', 'tag')


class LangPhrLink(models.Model):
    linking = models.ForeignKey(
        LangPhrPhrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
        related_name='linking',
    )

    linked = models.ForeignKey(
        LangPhrPhrase,
        verbose_name='被关联词语',
        on_delete=models.CASCADE,
        related_name='linked',
    )


class LangPhrGroup(models.Model):
    name = models.CharField(
        verbose_name='组名',
        unique=True,
    )


class LangPhrGroupSet(models.Model):
    group = models.ForeignKey(
        LangPhrGroup,
        verbose_name='关联组名',
        on_delete=models.CASCADE,
    )


class LangPhrGroupSetMember(models.Model):
    set = models.ForeignKey(
        LangPhrGroupSet,
        verbose_name='集合',
        on_delete=models.CASCADE,
    )

    phrase = models.ForeignKey(
        LangPhrPhrase,
        verbose_name='关联词语',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('set', 'phrase')
