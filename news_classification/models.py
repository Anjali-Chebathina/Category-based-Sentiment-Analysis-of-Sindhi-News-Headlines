# news_classification/models.py

from django.db import models
from accounts.models import CustomUser

class CategoryModel(models.Model):
    MODEL_TYPE_CHOICES = [
        ('svm', 'Support Vector Machine'),
        ('random_forest', 'Random Forest'),
        ('naive_bayes', 'Naive Bayes'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    model_file = models.FileField(upload_to='models/classification/')
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
