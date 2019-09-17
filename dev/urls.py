from django.urls import path, include

urlpatterns = [
    path('language/', include('dev.Language.urls'))
]
