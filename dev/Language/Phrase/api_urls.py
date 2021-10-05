from django.urls import path

from dev.Language.Phrase.api_views import PhraseView, TagView, ContributorView, ReviewView

urlpatterns = [
    path('', PhraseView.as_view()),
    path('tag', TagView.as_view()),
    path('contributor', ContributorView.as_view()),
    path('review', ReviewView.as_view()),
]
