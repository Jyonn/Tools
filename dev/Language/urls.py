from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('phrase', TemplateView.as_view(template_name='Language/phrase.html')),
]
