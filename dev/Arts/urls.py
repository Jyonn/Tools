from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('foto', TemplateView.as_view(template_name='Arts/foto.html'))
]
