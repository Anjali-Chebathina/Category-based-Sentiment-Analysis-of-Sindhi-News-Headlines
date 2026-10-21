# explainability/urls.py

from django.urls import path
from . import views

app_name = 'explainability'

urlpatterns = [
    path('explain/', views.explain_prediction, name='explain'),
]
