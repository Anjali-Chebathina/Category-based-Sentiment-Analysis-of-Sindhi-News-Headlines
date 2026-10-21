# sentiment_analysis/preprocessing.py

import re
import string
from typing import List

class SindhiTextPreprocessor:
    """
    Preprocessing utilities for Sindhi text
    """
    
    def __init__(self):
        # Sindhi-specific patterns
        self.arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670]')  # Remove diacritics
        
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        return re.sub(r'http\S+|www.\S+', '', text)
    
    def remove_mentions_hashtags(self, text: str) -> str:
        """Remove @mentions and #hashtags"""
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        return text
    
    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation"""
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_extra_spaces(self, text: str) -> str:
        """Remove extra whitespaces"""
        return ' '.join(text.split())
    
    def remove_diacritics(self, text: str) -> str:
        """Remove Arabic/Sindhi diacritics"""
        return self.arabic_diacritics.sub('', text)
    
    def normalize_text(self, text: str) -> str:
        """Normalize Sindhi text"""
        # Remove specific characters that might cause issues
        text = text.replace('ـ', '')  # Remove tatweel
        return text
    
    def preprocess(self, text: str, remove_punct: bool = False) -> str:
        """
        Complete preprocessing pipeline
        """
        if not text:
            return ""
        
        text = self.remove_urls(text)
        text = self.remove_mentions_hashtags(text)
        text = self.remove_diacritics(text)
        text = self.normalize_text(text)
        
        if remove_punct:
            text = self.remove_punctuation(text)
        
        text = self.remove_extra_spaces(text)
        
        return text.strip()
