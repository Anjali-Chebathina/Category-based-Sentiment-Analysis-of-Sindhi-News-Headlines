# explainability/admin.py

from django.contrib import admin
from .models import ExplanationHistory

@admin.register(ExplanationHistory)
class ExplanationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_class', 'confidence', 'created_at']
    list_filter = ['predicted_class', 'created_at']
    search_fields = ['user__username', 'input_text']
    readonly_fields = ['feature_weights']
