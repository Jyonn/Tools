from SmartDjango import models, E

from Base.operation import O


@E.register()
class IPError:
    IP_NOT_FOUND = E("找不到IP[{0}]")
    CREATE_IP = E("增加IP[{0}]失败")
    GET_IP = E("查找IP[{0}]失败")


class IP(models.Model):
    ip_start = models.PositiveIntegerField(
        verbose_name='IP起始整型值',
    )

    ip_end = models.PositiveIntegerField(
        verbose_name='IP结束整型值',
    )

    country = models.CharField(
        verbose_name='国家或地区',
        max_length=10,
    )

    province = models.CharField(
        verbose_name='省份',
        max_length=10,
    )

    city = models.CharField(
        verbose_name='城市',
        max_length=20,
    )

    owner = models.CharField(
        verbose_name='所有者',
        max_length=40,
    )

    line = models.CharField(
        verbose_name='线路',
        max_length=30,
    )

    @classmethod
    def new(cls, ip_start, ip_end, country, province, city, owner, line):
        locals_ = locals()
        del locals_['cls']

        cls.validator(locals_)

        try:
            ip = cls(**locals_)
            ip.save()
            return ip
        except Exception as err:
            raise IPError.CREATE_IP(
                '%s, %s' % (O.ip_int2dot(ip_start), O.ip_int2dot(ip_end)), debug_message=err)

    @classmethod
    def lookup(cls, ip):
        try:
            return cls.objects.get(ip_start__lte=ip, ip_end__gte=ip)
        except cls.DoesNotExist:
            raise IPError.IP_NOT_FOUND(O.ip_int2dot(ip))
        except Exception as err:
            raise IPError.GET_IP(O.ip_int2dot(ip), debug_message=err)

    def _readable_ip_start(self):
        return O.ip_int2dot(self.ip_start)

    def _readable_ip_end(self):
        return O.ip_int2dot(self.ip_end)

    def d(self):
        return self.dictor('ip_start', 'ip_end', 'country', 'province', 'city', 'owner', 'line')
