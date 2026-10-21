# admin_dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta

from accounts.models import CustomUser
from news_dataset.models import NewsCategory, SindhiNewsHeadline, AnalysisHistory
from sentiment_analysis.model_handler import SentimentAnalyzer
from news_classification.classifier import NewsClassifier
from .models import ModelPerformance, SystemLog

def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@admin_required
def admin_dashboard(request):
    """
    Main admin dashboard with statistics and charts
    """
    # Get statistics
    total_users = CustomUser.objects.filter(role='user').count()
    total_admins = CustomUser.objects.filter(role='admin').count()
    total_headlines = SindhiNewsHeadline.objects.count()
    total_categories = NewsCategory.objects.count()
    total_analyses = AnalysisHistory.objects.count()
    
    # Recent analyses
    recent_analyses = AnalysisHistory.objects.select_related('user')[:10]
    
    # Category distribution
    category_stats = SindhiNewsHeadline.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Sentiment distribution
    sentiment_stats = SindhiNewsHeadline.objects.values('sentiment').annotate(
        count=Count('id')
    ).order_by('sentiment')
    
    # User activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    daily_activity = AnalysisHistory.objects.filter(
        analysis_timestamp__gte=week_ago
    ).extra(
        select={'day': 'DATE(analysis_timestamp)'}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    # Recent logs
    recent_logs = SystemLog.objects.all()[:5]
    
    # Model performance
    recent_models = ModelPerformance.objects.all()[:5]
    
    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_headlines': total_headlines,
        'total_categories': total_categories,
        'total_analyses': total_analyses,
        'recent_analyses': recent_analyses,
        'category_stats': category_stats,
        'sentiment_stats': sentiment_stats,
        'daily_activity': daily_activity,
        'recent_logs': recent_logs,
        'recent_models': recent_models,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
@admin_required
def train_sentiment_model(request):
    """
    Train sentiment analysis model
    """
    if request.method == 'POST':
        try:
            # Get training data
            headlines = SindhiNewsHeadline.objects.filter(sentiment__isnull=False)
            
            if headlines.count() < 20:
                messages.error(request, 'Not enough labeled data. Need at least 20 headlines.')
                return redirect('admin_dashboard:dashboard')
            
            texts = [h.headline for h in headlines]
            labels = [h.sentiment for h in headlines]
            
            # Train model
            analyzer = SentimentAnalyzer(model_type='naive_bayes')
            metrics = analyzer.train(texts, labels)
            
            # Save performance
            ModelPerformance.objects.create(
                model_name='Naive Bayes Sentiment',
                model_type='sentiment',
                accuracy=metrics['accuracy'],
                f1_score=metrics['f1_score'],
                training_size=len(texts),
                trained_by=request.user
            )
            
            # Log
            SystemLog.objects.create(
                level='INFO',
                message=f'Sentiment model trained. Accuracy: {metrics["accuracy"]:.2%}',
                user=request.user
            )
            
            messages.success(request, f'Model trained successfully! Accuracy: {metrics["accuracy"]:.2%}')
            
        except Exception as e:
            messages.error(request, f'Error training model: {str(e)}')
            SystemLog.objects.create(
                level='ERROR',
                message=f'Model training failed: {str(e)}',
                user=request.user
            )
    
    return redirect('admin_dashboard:dashboard')

@login_required
@admin_required
def train_classification_model(request):
    """
    Train news classification model
    """
    if request.method == 'POST':
        try:
            # Get training data
            headlines = SindhiNewsHeadline.objects.filter(category__isnull=False)
            
            if headlines.count() < 20:
                messages.error(request, 'Not enough labeled data. Need at least 20 headlines.')
                return redirect('admin_dashboard:dashboard')
            
            texts = [h.headline for h in headlines]
            labels = [h.category.name for h in headlines]
            
            # Train model
            classifier = NewsClassifier()
            metrics = classifier.train(texts, labels)
            
            # Save performance
            ModelPerformance.objects.create(
                model_name='SVM News Classifier',
                model_type='classification',
                accuracy=metrics['accuracy'],
                f1_score=metrics['f1_score'],
                training_size=len(texts),
                trained_by=request.user
            )
            
            # Log
            SystemLog.objects.create(
                level='INFO',
                message=f'Classification model trained. Accuracy: {metrics["accuracy"]:.2%}',
                user=request.user
            )
            
            messages.success(request, f'Model trained successfully! Accuracy: {metrics["accuracy"]:.2%}')
            
        except Exception as e:
            messages.error(request, f'Error training model: {str(e)}')
            SystemLog.objects.create(
                level='ERROR',
                message=f'Model training failed: {str(e)}',
                user=request.user
            )
    
    return redirect('admin_dashboard:dashboard')

@login_required
@admin_required
def manage_users(request):
    """
    Manage system users
    """
    users = CustomUser.objects.all().order_by('-date_joined')
    
    context = {
        'users': users
    }
    
    return render(request, 'admin_dashboard/manage_users.html', context)

@login_required
@admin_required
def manage_dataset(request):
    """
    Manage news dataset
    """
    if request.method == 'POST':
        # Handle bulk upload
        csv_file = request.FILES.get('csv_file')
        
        if csv_file:
            try:
                import csv
                from io import TextIOWrapper
                
                file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_reader = csv.DictReader(file_data)
                
                count = 0
                for row in csv_reader:
                    headline = row.get('headline', '')
                    category_name = row.get('category', '')
                    sentiment = row.get('sentiment', '')
                    
                    if headline:
                        category = None
                        if category_name:
                            category, _ = NewsCategory.objects.get_or_create(name=category_name)
                        
                        SindhiNewsHeadline.objects.create(
                            headline=headline,
                            category=category,
                            sentiment=sentiment if sentiment else None,
                            added_by=request.user
                        )
                        count += 1
                
                messages.success(request, f'Successfully imported {count} headlines.')
                SystemLog.objects.create(
                    level='INFO',
                    message=f'Imported {count} headlines from CSV',
                    user=request.user
                )
                
            except Exception as e:
                messages.error(request, f'Error importing CSV: {str(e)}')
    
    headlines = SindhiNewsHeadline.objects.all().order_by('-created_at')[:50]
    categories = NewsCategory.objects.all()
    
    context = {
        'headlines': headlines,
        'categories': categories
    }
    
    return render(request, 'admin_dashboard/manage_dataset.html', context)

@login_required
@admin_required
def export_analysis_results(request):
    """
    Export analysis results to CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="analysis_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Input Text', 'Predicted Sentiment', 'Predicted Category', 'Confidence Score', 'Timestamp'])
    
    analyses = AnalysisHistory.objects.select_related('user').all()
    
    for analysis in analyses:
        writer.writerow([
            analysis.id,
            analysis.user.username,
            analysis.input_text,
            analysis.predicted_sentiment,
            analysis.predicted_category,
            analysis.confidence_score,
            analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    SystemLog.objects.create(
        level='INFO',
        message='Analysis results exported to CSV',
        user=request.user
    )
    
    return response

@login_required
@admin_required
def system_logs(request):
    """
    View system logs
    """
    logs = SystemLog.objects.all()[:100]
    
    context = {
        'logs': logs
    }
    
    return render(request, 'admin_dashboard/system_logs.html', context)
