# sentiment_analysis/model_handler.py - UPDATED VERSION

import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.calibration import CalibratedClassifierCV
from django.conf import settings
from .preprocessing import SindhiTextPreprocessor

class SentimentAnalyzer:
    """
    Sentiment Analysis with improved confidence scores
    """
    
    def __init__(self, model_type='logistic_regression'):
        self.model_type = model_type
        self.preprocessor = SindhiTextPreprocessor()
        
        # Improved TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=3000,
            min_df=1,
            max_df=0.85,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        
        self.model = None
        self.model_dir = os.path.join(settings.BASE_DIR, 'sentiment_analysis', 'ml_models')
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize model based on type
        if model_type == 'naive_bayes':
            self.model = MultinomialNB(alpha=0.1)
        elif model_type == 'logistic_regression':
            self.model = LogisticRegression(
                max_iter=1000,
                C=1.0,
                random_state=42,
                class_weight='balanced'
            )
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=150,
                max_depth=15,
                random_state=42,
                class_weight='balanced'
            )
    
    def train(self, texts: list, labels: list):
        """
        Train sentiment analysis model
        """
        # Preprocess texts
        processed_texts = [self.preprocessor.preprocess(text) for text in texts]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            processed_texts, labels, 
            test_size=0.2, 
            random_state=42, 
            stratify=labels
        )
        
        # Transform to TF-IDF features
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        # Train model
        self.model.fit(X_train_tfidf, y_train)
        
        # Calibrate for better probabilities
        if self.model_type == 'naive_bayes':
            self.model = CalibratedClassifierCV(self.model, cv=3, method='isotonic')
            self.model.fit(X_train_tfidf, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_tfidf)
        y_proba = self.model.predict_proba(X_test_tfidf)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Average confidence
        avg_confidence = np.mean(np.max(y_proba, axis=1)) * 100
        
        # Save model and vectorizer
        self.save_model()
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'avg_confidence': avg_confidence,
            'classification_report': classification_report(y_test, y_pred)
        }
    
    def predict(self, text: str):
        """
        Predict sentiment with proper confidence
        """
        if self.model is None:
            self.load_model()
        
        # Preprocess
        processed_text = self.preprocessor.preprocess(text)
        
        # Transform
        text_tfidf = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(text_tfidf)[0]
        
        # Get probability scores
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(text_tfidf)[0]
            confidence = float(max(probabilities) * 100)
            
            # Get all class probabilities
            class_probabilities = {}
            for i, label in enumerate(self.model.classes_):
                class_probabilities[label] = float(probabilities[i] * 100)
        else:
            confidence = 0.0
            class_probabilities = {}
        
        return {
            'sentiment': prediction,
            'confidence': confidence,
            'all_probabilities': class_probabilities
        }
    
    def save_model(self):
        """Save trained model and vectorizer"""
        model_path = os.path.join(self.model_dir, f'sentiment_model_{self.model_type}.pkl')
        vectorizer_path = os.path.join(self.model_dir, f'tfidf_vectorizer_{self.model_type}.pkl')
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_model(self):
        """Load pre-trained model and vectorizer"""
        model_path = os.path.join(self.model_dir, f'sentiment_model_{self.model_type}.pkl')
        vectorizer_path = os.path.join(self.model_dir, f'tfidf_vectorizer_{self.model_type}.pkl')
        
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            return True
        except FileNotFoundError:
            return False
