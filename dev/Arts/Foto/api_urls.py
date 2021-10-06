from django.urls import path

from dev.Arts.Foto import api_views as views

urlpatterns = [
    path('callback', views.CallbackView.as_view()),
    path('token', views.TokenView.as_view()),
    path('<str:foto>', views.FotoView.as_view()),
    path('', views.HomeView.as_view()),
    path('album/<str:album>', views.AlbumView.as_view()),
]
