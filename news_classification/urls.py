# news_classification/urls.py

from django.urls import path
from . import views

app_name = 'news_classification'

urlpatterns = [
    path('classify/', views.classify_news, name='classify'),
]
