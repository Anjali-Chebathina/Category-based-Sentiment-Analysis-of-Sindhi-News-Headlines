# sentiment_analysis/forms.py

from django import forms

class SentimentAnalysisForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter Sindhi news headline here...'
        }),
        label='News Headline',
        help_text='Enter a Sindhi news headline to analyze its sentiment'
    )
