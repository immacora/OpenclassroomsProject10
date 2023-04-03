from django.urls import path
from django.views.generic import TemplateView

app_name = 'projects'

urlpatterns = [
    path('', TemplateView.as_view(template_name="projects/index.html")),
]