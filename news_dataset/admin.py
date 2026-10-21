# news_dataset/admin.py

from django.contrib import admin
from .models import NewsCategory, SindhiNewsHeadline, AnalysisHistory

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(SindhiNewsHeadline)
class SindhiNewsHeadlineAdmin(admin.ModelAdmin):
    list_display = ['headline', 'category', 'sentiment', 'created_at']
    list_filter = ['category', 'sentiment', 'created_at']
    search_fields = ['headline']

@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_sentiment', 'predicted_category', 'confidence_score', 'analysis_timestamp']
    list_filter = ['predicted_sentiment', 'predicted_category', 'analysis_timestamp']
    search_fields = ['user__username', 'input_text']
