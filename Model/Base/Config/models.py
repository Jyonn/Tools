from SmartDjango import ErrorJar, models, Excp, E


@ErrorJar.pour
class ConfigError:
    CREATE_CONFIG = E("更新配置错误", hc=500)
    CONFIG_NOT_FOUND = E("不存在的配置", hc=404)


class Config(models.Model):
    key = models.CharField(
        max_length=100,
        unique=True,
    )

    value = models.CharField(
        max_length=255,
    )

    @classmethod
    @Excp.pack
    def get_config_by_key(cls, key):
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist:
            return ConfigError.CONFIG_NOT_FOUND

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            return cls.get_config_by_key(key).value
        except Exception:
            return default

    @classmethod
    @Excp.pack
    def update_value(cls, key, value):
        cls.validator(locals())

        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except Excp as ret:
            if ret.eis(ConfigError.CONFIG_NOT_FOUND):
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception:
                    return ConfigError.CREATE_CONFIG
            else:
                return ConfigError.CREATE_CONFIG


class ConfigInstance:
    pass


CI = ConfigInstance
