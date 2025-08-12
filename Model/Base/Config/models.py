from django.db import models
from smartdjango import Error

from Model.Base.Config.validators import ConfigErrors, ConfigValidator


class Config(models.Model):
    vldt = ConfigValidator

    key = models.CharField(
        max_length=vldt.MAX_KEY_LENGTH,
        unique=True,
        validators=[vldt.key],
    )

    value = models.CharField(
        max_length=vldt.MAX_VALUE_LENGTH,
        validators=[vldt.value],
    )

    @classmethod
    def get_config_by_key(cls, key) -> 'Config':
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigErrors.NOT_FOUND(details=err)

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            return cls.get_config_by_key(key).value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except Error as e:
            if e == ConfigErrors.NOT_FOUND:
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception as err:
                    raise ConfigErrors.CREATE(details=err)
            else:
                raise e
        except Exception as err:
            raise ConfigErrors.CREATE(details=err)


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

    VPNNET_LOGIN_URL = 'VPNNet-LOGIN-URL'
    VPNNET_LOG_URL = 'VPNNet-LOG-URL'
    VPNNET_EMAIL = 'VPNNET-EMAIL'
    VPNNET_PASSWORD = 'VPNNET-PASSWORD'
    VPNNET_LAST_CHECK = 'VPNNET-LAST-CHECK'
    VPNNET_CHECK_INTERVAL = 'VPNNET-CHECK-INTERVAL'


CI = ConfigInstance
