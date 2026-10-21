# explainability/forms.py

from django import forms

class ExplainForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter Sindhi news headline to get explanation...'
        }),
        label='News Headline',
        help_text='Enter text to see which words influenced the prediction'
    )
