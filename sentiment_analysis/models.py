# sentiment_analysis/models.py

from django.db import models
from accounts.models import CustomUser

class SentimentModel(models.Model):
    MODEL_TYPE_CHOICES = [
        ('naive_bayes', 'Naive Bayes'),
        ('logistic_regression', 'Logistic Regression'),
        ('transformer', 'Transformer'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    model_file = models.FileField(upload_to='models/sentiment/')
    vectorizer_file = models.FileField(upload_to='models/vectorizers/', blank=True, null=True)
    accuracy = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=False)
    trained_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_model_type_display()})"
    
    class Meta:
        ordering = ['-created_at']
