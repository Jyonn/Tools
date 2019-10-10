from SmartDjango import models, Excp, E, ErrorJar

from Base.operation import O


@ErrorJar.pour
class IPError:
    IP_NOT_FOUND = E("找不到IP[{0}]", ph=E.PH_FORMAT)
    CREATE_IP = E("增加IP[{0}]失败", ph=E.PH_FORMAT)
    GET_IP = E("查找IP[{0}]失败", ph=E.PH_FORMAT)


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
    @Excp.pack
    def new(cls, ip_start, ip_end, country, province, city, owner, line):
        locals_ = locals()
        del locals_['cls']

        cls.validator(locals_)

        try:
            ip = cls(**locals_)
            ip.save()
            return ip
        except Exception:
            return IPError.CREATE_IP('%s, %s' % (O.ip_int2dot(ip_start), O.ip_int2dot(ip_end)))

    @classmethod
    @Excp.pack
    def lookup(cls, ip):
        try:
            return cls.objects.get(ip_start__lte=ip, ip_end__gte=ip)
        except cls.DoesNotExist:
            return IPError.IP_NOT_FOUND(O.ip_int2dot(ip))
        except Exception:
            return IPError.GET_IP(O.ip_int2dot(ip))

    def _readable_ip_start(self):
        return O.ip_int2dot(self.ip_start)

    def _readable_ip_end(self):
        return O.ip_int2dot(self.ip_end)

    def d(self):
        return self.dictor('ip_start', 'ip_end', 'country', 'province', 'city', 'owner', 'line')
