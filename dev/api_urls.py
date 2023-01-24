from django.urls import path, include

urlpatterns = [
    path('language/', include('dev.Language.api_urls')),
    path('arts/', include('dev.Arts.api_urls')),
    path('network/', include('dev.Network.api_urls')),
]
