from django.urls import path, include

urlpatterns = [
    path('language/', include('dev.Language.urls')),
    path('arts/', include('dev.Arts.urls')),
]
