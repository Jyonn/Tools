from Model.Base.Config.models import Config, CI

EMAIL = Config.get_value_by_key(CI.VPNNET_EMAIL)
PASSWORD = Config.get_value_by_key(CI.VPNNET_PASSWORD)
CHECK_INTERVAL = int(Config.get_value_by_key(CI.VPNNET_CHECK_INTERVAL) or 0)
LOGIN_URL = Config.get_value_by_key(CI.VPNNET_LOGIN_URL)
LOG_URL = Config.get_value_by_key(CI.VPNNET_LOG_URL)
