# explainability/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .lime_explainer import ExplainabilityHandler
from .forms import ExplainForm

@login_required
def explain_prediction(request):
    """
    Explain predictions using LIME
    """
    explanation = None
    
    if request.method == 'POST':
        form = ExplainForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            
            try:
                # Initialize explainer
                explainer = ExplainabilityHandler(task='sentiment')
                
                # Get explanation
                explanation = explainer.explain_prediction(text, num_features=10)
                
                messages.success(request, 'Explanation generated successfully!')
            except Exception as e:
                messages.error(request, f'Error generating explanation: {str(e)}')
    else:
        form = ExplainForm()
    
    context = {
        'form': form,
        'explanation': explanation
    }
    
    return render(request, 'explainability/explain.html', context)
