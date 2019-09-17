from django.urls import re_path

from App.Language.views import languageRouter
from Base.router import Router

router = Router()
router.register('language', languageRouter.as_handler().rename('语言类应用', '包含押韵、拼音转换等API'))

urlpatterns = [
    re_path('^(?P<path>(.*?)+)$', router.route),
]
