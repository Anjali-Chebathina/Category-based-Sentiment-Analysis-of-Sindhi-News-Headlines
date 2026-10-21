# sentiment_analysis/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from news_dataset.models import SindhiNewsHeadline, AnalysisHistory
from .model_handler import SentimentAnalyzer
from .forms import SentimentAnalysisForm

@login_required
def analyze_sentiment(request):
    """
    Main sentiment analysis view
    """
    result = None
    
    if request.method == 'POST':
        form = SentimentAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            
            # Initialize analyzer
            analyzer = SentimentAnalyzer(model_type='naive_bayes')
            
            # Check if model exists, otherwise train it
            if not analyzer.load_model():
                messages.warning(request, 'Model not trained yet. Training with available data...')
                # Get training data from database
                headlines = SindhiNewsHeadline.objects.filter(sentiment__isnull=False)
                if headlines.count() > 10:
                    texts = [h.headline for h in headlines]
                    labels = [h.sentiment for h in headlines]
                    metrics = analyzer.train(texts, labels)
                    messages.success(request, f'Model trained! Accuracy: {metrics["accuracy"]:.2%}')
                else:
                    messages.error(request, 'Not enough training data available.')
                    return render(request, 'sentiment_analysis/analyze.html', {'form': form})
            
            # Perform prediction
            result = analyzer.predict(text)
            
            # Save to history
            AnalysisHistory.objects.create(
                user=request.user,
                input_text=text,
                predicted_sentiment=result['sentiment'],
                predicted_category='',
                confidence_score=result['confidence']
            )
            
            messages.success(request, 'Sentiment analysis completed!')
    else:
        form = SentimentAnalysisForm()
    
    # Get recent analyses
    recent_analyses = AnalysisHistory.objects.filter(user=request.user)[:5]
    
    context = {
        'form': form,
        'result': result,
        'recent_analyses': recent_analyses
    }
    
    return render(request, 'sentiment_analysis/analyze.html', context)

@login_required
def dataset_analysis(request):
    """
    Analyze headlines from dataset
    """
    headlines = SindhiNewsHeadline.objects.all()[:20]
    
    context = {
        'headlines': headlines
    }
    
    return render(request, 'sentiment_analysis/dataset_analysis.html', context)

@login_required
def analyze_single_headline(request, headline_id):
    """
    Analyze a single headline from dataset
    """
    try:
        headline = SindhiNewsHeadline.objects.get(id=headline_id)
        
        analyzer = SentimentAnalyzer(model_type='naive_bayes')
        if not analyzer.load_model():
            messages.error(request, 'Model not trained yet.')
            return redirect('sentiment_analysis:analyze')
        
        result = analyzer.predict(headline.headline)
        
        # Save to history
        AnalysisHistory.objects.create(
            user=request.user,
            headline=headline,
            input_text=headline.headline,
            predicted_sentiment=result['sentiment'],
            predicted_category=headline.category.name if headline.category else '',
            confidence_score=result['confidence']
        )
        
        messages.success(request, f'Predicted sentiment: {result["sentiment"]} (Confidence: {result["confidence"]:.2%})')
        
    except SindhiNewsHeadline.DoesNotExist:
        messages.error(request, 'Headline not found.')
    
    return redirect('sentiment_analysis:dataset_analysis')
