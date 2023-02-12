from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('vpnnet', TemplateView.as_view(template_name='Network/vpnnet.html')),
]
