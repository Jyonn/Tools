from SmartDjango import models, E, Hc


@E.register()
class ConfigError:
    CREATE_CONFIG = E("更新配置错误", hc=Hc.InternalServerError)
    CONFIG_NOT_FOUND = E("不存在的配置", hc=Hc.NotFound)


class Config(models.Model):
    key = models.CharField(
        max_length=100,
        unique=True,
    )

    value = models.CharField(
        max_length=255,
    )

    @classmethod
    def get_config_by_key(cls, key):
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigError.CONFIG_NOT_FOUND(debug_message=err)

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            return cls.get_config_by_key(key).value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        cls.validator(locals())

        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except E as e:
            if e.eis(ConfigError.CONFIG_NOT_FOUND):
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception as err:
                    raise ConfigError.CREATE_CONFIG(debug_message=err)
            else:
                raise e
        except Exception as err:
            raise ConfigError.CREATE_CONFIG(debug_message=err)


class ConfigInstance:
    LibBooking_BD_APP_ID = "LibBooking-BD-APP-ID"
    LibBooking_BD_APP_KEY = "LibBooking-BD-APP-KEY"
    LibBooking_BD_APP_SECRET = "LibBooking-BD-APP-SECRET"

    FOTO_QN_ACCESS_KEY = 'Foto-QN-ACCESS-KEY'
    FOTO_QN_SECRET_KEY = 'Foto-QN-SECRET-KEY'
    FOTO_QN_RES_BUCKET = 'Foto-QN-RES-BUCKET'
    FOTO_QN_CDN_HOST = 'Foto-QN-CDN-HOST'
    FOTO_ADMIN_TOKEN = 'Foto-ADMIN-TOKEN'
    FOTO_MAX_IMAGE_SIZE = 'Foto-MAX-IMAGE-SIZE'


CI = ConfigInstance
