# admin_dashboard/models.py

from django.db import models
from accounts.models import CustomUser

class ModelPerformance(models.Model):
    MODEL_TYPES = [
        ('sentiment', 'Sentiment Analysis'),
        ('classification', 'News Classification'),
    ]
    
    model_name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    accuracy = models.FloatField()
    f1_score = models.FloatField()
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    training_size = models.IntegerField()
    trained_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    trained_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.model_name} - {self.accuracy:.2%}"
    
    class Meta:
        ordering = ['-trained_at']

class SystemLog(models.Model):
    LOG_LEVELS = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]
    
    level = models.CharField(max_length=10, choices=LOG_LEVELS)
    message = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.level} - {self.message[:50]}"
    
    class Meta:
        ordering = ['-timestamp']
