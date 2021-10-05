from django.urls import path, include

urlpatterns = [
    path('phrase/', include('dev.Language.Phrase.api_urls')),
]
