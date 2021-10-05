from django.urls import path

from dev.Arts.Foto.api_views import CallbackView, TokenView, HomeView, AlbumView

urlpatterns = [
    path('callback', CallbackView.as_view()),
    path('token', TokenView.as_view()),
    path('', HomeView.as_view()),
    path('album/<str:album>', AlbumView.as_view()),
]
