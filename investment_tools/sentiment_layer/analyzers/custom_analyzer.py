from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List
from .base_sentiment_analyzer import BaseSentimentAnalyzer

class FinBERTAnalyzer(BaseSentimentAnalyzer):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.pipeline = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

    def analyze(self, texts: List[str]) -> List[dict]:
        return self.pipeline(texts)
