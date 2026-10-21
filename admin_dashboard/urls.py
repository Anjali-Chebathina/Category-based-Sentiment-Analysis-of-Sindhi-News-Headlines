# admin_dashboard/urls.py

from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('train-sentiment/', views.train_sentiment_model, name='train_sentiment'),
    path('train-classification/', views.train_classification_model, name='train_classification'),
    path('users/', views.manage_users, name='manage_users'),
    path('dataset/', views.manage_dataset, name='manage_dataset'),
    path('export-results/', views.export_analysis_results, name='export_results'),
    path('logs/', views.system_logs, name='system_logs'),
]
