# sentiment_analysis/admin.py

from django.contrib import admin
from .models import SentimentModel

@admin.register(SentimentModel)
class SentimentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'accuracy', 'f1_score', 'is_active', 'created_at']
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.trained_by = request.user
        super().save_model(request, obj, form, change)
