# admin_dashboard/admin.py

from django.contrib import admin
from .models import ModelPerformance, SystemLog

@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_type', 'accuracy', 'f1_score', 'training_size', 'trained_at']
    list_filter = ['model_type', 'trained_at']
    search_fields = ['model_name']

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['level', 'message', 'user', 'timestamp']
    list_filter = ['level', 'timestamp']
    search_fields = ['message']
