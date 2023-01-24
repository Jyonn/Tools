from django.urls import path

from dev.Network.VPNNet import api_views as views

urlpatterns = [
    path('retrieve', views.UpdateView.as_view()),
]
