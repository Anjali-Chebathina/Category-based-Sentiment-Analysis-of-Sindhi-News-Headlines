# explainability/models.py

from django.db import models
from accounts.models import CustomUser

class ExplanationHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    input_text = models.TextField()
    predicted_class = models.CharField(max_length=50)
    confidence = models.FloatField()
    feature_weights = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.predicted_class}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Explanation Histories'
