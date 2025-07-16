from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_with_vader(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using VADER"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return {
                'compound': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        except Exception as e:
            logger.error(f"Error in VADER analysis: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def analyze_with_textblob(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity
            }
        except Exception as e:
            logger.error(f"Error in TextBlob analysis: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.0}
    
    def analyze(self, text: str) -> Dict[str, any]:
        """Comprehensive sentiment analysis"""
        if not text or not text.strip():
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0
            }
        
        # Clean text
        text = text.strip()
        
        # VADER analysis
        vader_scores = self.analyze_with_vader(text)
        
        # TextBlob analysis
        textblob_scores = self.analyze_with_textblob(text)
        
        # Combine scores for final sentiment
        vader_compound = vader_scores['compound']
        textblob_polarity = textblob_scores['polarity']
        
        # Weighted average (VADER is better for social media/news text)
        combined_score = (vader_compound * 0.7) + (textblob_polarity * 0.3)
        
        # Determine sentiment category
        if combined_score >= 0.05:
            sentiment = 'positive'
        elif combined_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Calculate confidence based on score magnitude
        confidence = min(abs(combined_score), 1.0)
        
        return {
            'sentiment': sentiment,
            'score': round(combined_score, 3),
            'confidence': round(confidence, 3),
            'vader_scores': vader_scores,
            'textblob_scores': textblob_scores
        }
    
    def batch_analyze(self, texts: list) -> list:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        return results