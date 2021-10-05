from django.urls import path, include

urlpatterns = [
    path('foto/', include('dev.Arts.Foto.api_urls'))
]
