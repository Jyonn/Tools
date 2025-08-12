from diq import Dictify
from django.db import models

from Base.operation import O
from Model.Network.IP.validators import IPValidator, IPErrors


class IP(models.Model, Dictify):
    vldt = IPValidator

    ip_start = models.PositiveIntegerField(
        verbose_name='IP起始整型值',
    )

    ip_end = models.PositiveIntegerField(
        verbose_name='IP结束整型值',
    )

    country = models.CharField(
        verbose_name='国家或地区',
        max_length=vldt.MAX_COUNTRY_LENGTH,
    )

    province = models.CharField(
        verbose_name='省份',
        max_length=vldt.MAX_PROVINCE_LENGTH,
    )

    city = models.CharField(
        verbose_name='城市',
        max_length=vldt.MAX_CITY_LENGTH,
    )

    owner = models.CharField(
        verbose_name='所有者',
        max_length=vldt.MAX_OWNER_LENGTH,
    )

    line = models.CharField(
        verbose_name='线路',
        max_length=vldt.MAX_LINE_LENGTH,
    )

    @classmethod
    def new(cls, ip_start, ip_end, country, province, city, owner, line):
        locals_ = locals()
        del locals_['cls']

        # cls.validator(locals_)
        # TODO: validator

        try:
            ip = cls(**locals_)
            ip.save()
            return ip
        except Exception as err:
            raise IPErrors.CREATE_IP(
                '%s, %s' % (O.ip_int2dot(ip_start), O.ip_int2dot(ip_end)), details=err)

    @classmethod
    def lookup(cls, ip):
        try:
            return cls.objects.get(ip_start__lte=ip, ip_end__gte=ip)
        except cls.DoesNotExist:
            raise IPErrors.IP_NOT_FOUND(O.ip_int2dot(ip))
        except Exception as err:
            raise IPErrors.GET_IP(O.ip_int2dot(ip), details=err)

    def _dictify_ip_start(self):
        return O.ip_int2dot(self.ip_start)

    def _dictify_ip_end(self):
        return O.ip_int2dot(self.ip_end)

    def d(self):
        return self.dictify('ip_start', 'ip_end', 'country', 'province', 'city', 'owner', 'line')
