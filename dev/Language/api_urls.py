from django.urls import path

from dev.Language.api_views import PhraseView, TagView

urlpatterns = [
    path('phrase', PhraseView.as_view()),
    path('phrase/tag', TagView.as_view()),
]
