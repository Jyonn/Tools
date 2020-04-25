from django.urls import re_path

from App.Doris.views import dorisRouter
from App.Entertainment.views import entertainmentRouter
from App.Language.views import languageRouter
from App.Network.views import networkRouter
from Base.router import Router

router = Router()
router.register('language', languageRouter.as_handler().rename('语言类应用', '包含押韵、拼音转换等API'))
router.register('network', networkRouter.as_handler().rename('网络类应用', '包含IP查询等API'))
router.register('entertainment', entertainmentRouter.as_handler().rename('娱乐类应用', '包含朋友圈默契度偷窥等API'))
router.register('doris', dorisRouter.as_handler().rename('洋洋专用应用', '包含图书馆一键预约等API'))

urlpatterns = [
    re_path('^(?P<path>(.*?)+)$', router.route),
]
