import qiniu

from Base.qiniu.policy import Policy
from Base.qiniu.qn import QnManager
from Model.Base.Config.models import Config, CI

ACCESS_KEY = Config.get_value_by_key(CI.FOTO_QN_ACCESS_KEY)
SECRET_KEY = Config.get_value_by_key(CI.FOTO_QN_SECRET_KEY)
RES_BUCKET = Config.get_value_by_key(CI.FOTO_QN_RES_BUCKET)
RES_CDN_HOST = Config.get_value_by_key(CI.FOTO_QN_CDN_HOST)
ADMIN_TOKEN = Config.get_value_by_key(CI.FOTO_ADMIN_TOKEN)
MAX_IMAGE_SIZE = int(Config.get_value_by_key(CI.FOTO_MAX_IMAGE_SIZE))


try:
    AUTH = qiniu.Auth(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
except Exception as err:
    AUTH = None

qn_manager = QnManager(
    auth=AUTH,
    bucket=RES_BUCKET,
    cdn_host=RES_CDN_HOST,
    public=False,
    prefix='Foto/'
)
policy = Policy(
    callback_url='https://tools.6-79.cn/dev/arts/foto/callback',
    max_image_size=MAX_IMAGE_SIZE,
)


def boundary(max_=None, min_=None):
    def processor(value):
        value = int(value)
        if max_ is not None and value > max_:
            value = max_
        if min_ is not None and value < min_:
            value = min_
        return value
    return processor
