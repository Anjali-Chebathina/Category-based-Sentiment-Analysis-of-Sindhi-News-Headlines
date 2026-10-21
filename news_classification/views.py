# news_classification/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from news_dataset.models import SindhiNewsHeadline, AnalysisHistory
from .classifier import NewsClassifier
from .forms import ClassificationForm

# news_classification/views.py - UPDATE THIS PART

@login_required
def classify_news(request):
    """
    Main news classification view with improved confidence
    """
    result = None
    
    if request.method == 'POST':
        form = ClassificationForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            
            # Use Random Forest classifier
            classifier = NewsClassifier(model_type='random_forest')
            
            if not classifier.load_model():
                messages.warning(request, 'Model not trained. Training now...')
                headlines = SindhiNewsHeadline.objects.filter(category__isnull=False)
                if headlines.count() > 50:
                    texts = [h.headline for h in headlines]
                    labels = [h.category.name for h in headlines]
                    metrics = classifier.train(texts, labels)
                    messages.success(request, f'Trained! Accuracy: {metrics["accuracy"]:.2%}, Avg Confidence: {metrics["avg_confidence"]:.2f}%')
                else:
                    messages.error(request, 'Not enough training data.')
                    return render(request, 'news_classification/classify.html', {'form': form})
            
            # Perform prediction
            result = classifier.predict(text)
            
            # Save to history
            AnalysisHistory.objects.create(
                user=request.user,
                input_text=text,
                predicted_sentiment='',
                predicted_category=result['category'],
                confidence_score=result['confidence']
            )
            
            messages.success(request, 'Classification completed!')
    else:
        form = ClassificationForm()
    
    context = {
        'form': form,
        'result': result
    }
    
    return render(request, 'news_classification/classify.html', context)
