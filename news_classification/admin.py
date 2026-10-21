# news_classification/admin.py

from django.contrib import admin
from .models import CategoryModel

@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'accuracy', 'f1_score', 'is_active', 'created_at']
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name']
