from django.urls import path, include

urlpatterns = [
    path('view/', include('dev.urls')),
    path('api/', include('dev.api_urls')),
]
