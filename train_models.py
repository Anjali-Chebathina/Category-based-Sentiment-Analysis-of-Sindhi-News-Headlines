# train_models_final.py

import os
import django
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sindhi_news_project.settings')
django.setup()

from news_dataset.models import SindhiNewsHeadline
from sentiment_analysis.model_handler import SentimentAnalyzer
from news_classification.classifier import NewsClassifier
from admin_dashboard.models import ModelPerformance

def train_with_confidence_boost():
    print("\n" + "=" * 70)
    print("FINAL TRAINING - TARGET: 75-90% CONFIDENCE")
    print("=" * 70)
    
    # SENTIMENT MODEL
    print("\n📊 TRAINING SENTIMENT ANALYSIS MODEL...")
    print("-" * 70)
    
    headlines = SindhiNewsHeadline.objects.filter(sentiment__isnull=False)
    print(f"Training data: {headlines.count()} headlines")
    
    if headlines.count() < 300:
        print("⚠️  WARNING: Need at least 300 headlines for high confidence")
        print("   Please run: python create_mega_dataset.py")
        return
    
    texts = [h.headline for h in headlines]
    labels = [h.sentiment for h in headlines]
    
    # Count distribution
    from collections import Counter
    dist = Counter(labels)
    print(f"Distribution: {dict(dist)}")
    
    analyzer = SentimentAnalyzer(model_type='logistic_regression')
    metrics = analyzer.train(texts, labels)
    
    ModelPerformance.objects.create(
        model_name='Logistic Regression Sentiment (Final)',
        model_type='sentiment',
        accuracy=metrics['accuracy'],
        f1_score=metrics['f1_score'],
        training_size=len(texts),
    )
    
    print(f"\n✅ SENTIMENT MODEL RESULTS:")
    print(f"   Accuracy: {metrics['accuracy']:.2%}")
    print(f"   F1-Score: {metrics['f1_score']:.2%}")
    print(f"   Average Confidence: {metrics['avg_confidence']:.2f}%")
    
    # CLASSIFICATION MODEL
    print("\n📊 TRAINING CLASSIFICATION MODEL...")
    print("-" * 70)
    
    headlines = SindhiNewsHeadline.objects.filter(category__isnull=False)
    print(f"Training data: {headlines.count()} headlines")
    
    texts = [h.headline for h in headlines]
    labels = [h.category.name for h in headlines]
    
    dist = Counter(labels)
    print(f"Distribution: {dict(dist)}")
    
    classifier = NewsClassifier(model_type='random_forest')
    metrics = classifier.train(texts, labels)
    
    ModelPerformance.objects.create(
        model_name='Random Forest Classifier (Final)',
        model_type='classification',
        accuracy=metrics['accuracy'],
        f1_score=metrics['f1_score'],
        training_size=len(texts),
    )
    
    print(f"\n✅ CLASSIFICATION MODEL RESULTS:")
    print(f"   Accuracy: {metrics['accuracy']:.2%}")
    print(f"   F1-Score: {metrics['f1_score']:.2%}")
    print(f"   Average Confidence: {metrics['avg_confidence']:.2f}%")
    
    print("\n" + "=" * 70)
    if metrics['avg_confidence'] >= 70:
        print("🎉 SUCCESS! Confidence is now 70%+")
    else:
        print(f"⚠️  Current confidence: {metrics['avg_confidence']:.1f}%")
        print("   Recommendation: Add more training data")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    train_with_confidence_boost()
