from django.urls import path

from dev.Network.VPNNet import api_views as views

patterns = [
    path('retrieve', views.UpdateView.as_view()),
]
