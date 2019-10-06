from django.urls import re_path

from App.Language.views import languageRouter
from App.Network.views import networkRouter
from Base.router import Router

router = Router()
router.register('language', languageRouter.as_handler().rename('语言类应用', '包含押韵、拼音转换等API'))
router.register('network', networkRouter.as_handler().rename('网络类应用', '包含IP查询等API'))

urlpatterns = [
    re_path('^(?P<path>(.*?)+)$', router.route),
]
