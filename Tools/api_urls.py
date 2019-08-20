from django.urls import re_path

from Language.views import languageRouter


urlpatterns = [
    re_path('^language/(?P<path>(.*?)+)$', languageRouter.route),
]
