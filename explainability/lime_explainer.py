# explainability/lime_explainer.py

import os
import pickle
from lime.lime_text import LimeTextExplainer
from django.conf import settings
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sentiment_analysis.preprocessing import SindhiTextPreprocessor
from sentiment_analysis.model_handler import SentimentAnalyzer

class ExplainabilityHandler:
    """
    LIME-based explainability for sentiment analysis and classification
    """
    
    def __init__(self, task='sentiment'):
        self.task = task
        self.preprocessor = SindhiTextPreprocessor()
        
        if task == 'sentiment':
            self.analyzer = SentimentAnalyzer(model_type='naive_bayes')
            self.analyzer.load_model()
            self.class_names = ['negative', 'neutral', 'positive']
        
        # Initialize LIME explainer
        self.explainer = LimeTextExplainer(class_names=self.class_names)
    
    def predict_proba_wrapper(self, texts):
        """
        Wrapper function for LIME to get prediction probabilities
        """
        import numpy as np
        probas = []
        
        for text in texts:
            processed_text = self.preprocessor.preprocess(text)
            text_tfidf = self.analyzer.vectorizer.transform([processed_text])
            
            if hasattr(self.analyzer.model, 'predict_proba'):
                proba = self.analyzer.model.predict_proba(text_tfidf)[0]
            else:
                # For models without predict_proba, create dummy probabilities
                pred = self.analyzer.model.predict(text_tfidf)[0]
                proba = np.zeros(len(self.class_names))
                pred_idx = self.class_names.index(pred)
                proba[pred_idx] = 1.0
            
            probas.append(proba)
        
        return np.array(probas)
    
    def explain_prediction(self, text, num_features=10):
        """
        Generate LIME explanation for a prediction
        """
        # Get explanation
        exp = self.explainer.explain_instance(
            text, 
            self.predict_proba_wrapper,
            num_features=num_features,
            top_labels=3
        )
        
        # Get prediction
        result = self.analyzer.predict(text)
        predicted_class = result['sentiment']
        predicted_class_idx = self.class_names.index(predicted_class)
        
        # Get feature importance
        feature_weights = exp.as_list(label=predicted_class_idx)
        
        # Format explanation
        explanation = {
            'predicted_class': predicted_class,
            'confidence': result['confidence'],
            'feature_weights': feature_weights,
            'visualization_html': exp.as_html()
        }
        
        return explanation
