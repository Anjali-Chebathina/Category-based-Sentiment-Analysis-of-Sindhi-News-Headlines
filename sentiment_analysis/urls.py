# sentiment_analysis/urls.py

from django.urls import path
from . import views

app_name = 'sentiment_analysis'

urlpatterns = [
    path('analyze/', views.analyze_sentiment, name='analyze'),
    path('dataset/', views.dataset_analysis, name='dataset_analysis'),
    path('analyze-headline/<int:headline_id>/', views.analyze_single_headline, name='analyze_headline'),
]
