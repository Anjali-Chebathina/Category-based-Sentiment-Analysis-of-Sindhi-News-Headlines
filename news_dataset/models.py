# news_dataset/models.py

from django.db import models
from accounts.models import CustomUser

class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'News Categories'

class SindhiNewsHeadline(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    
    headline = models.TextField()
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.headline[:100]

    class Meta:
        ordering = ['-created_at']

class AnalysisHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    headline = models.ForeignKey(SindhiNewsHeadline, on_delete=models.SET_NULL, null=True, blank=True)
    input_text = models.TextField()
    predicted_sentiment = models.CharField(max_length=10)
    predicted_category = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0.0)
    analysis_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_sentiment}"

    class Meta:
        verbose_name_plural = 'Analysis Histories'
        ordering = ['-analysis_timestamp']
