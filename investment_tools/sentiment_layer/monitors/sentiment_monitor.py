from datetime import datetime
from typing import List, Dict
from sentiment_layer.analyzers.base_sentiment_analyzer import BaseSentimentAnalyzer
from sentiment_layer.utils.sentiment_models import NewsSentimentEntry
from sentiment_layer.data_sources.base_data_sources import BaseDataSource

class SentimentMonitor:
    def __init__(self, data_source: BaseDataSource, analyzer: BaseSentimentAnalyzer):
        self.data_source = data_source
        self.analyzer = analyzer
        self.sentiment_history: Dict[str, List[NewsSentimentEntry]] = {}

    def monitor(self, stock_symbols: List[str]):
        news_articles = self.data_source.fetch_news(stock_symbols)
        texts = [article['headline'] for article in news_articles]
        results = self.analyzer.analyze(texts)

        for article, result in zip(news_articles, results):
            entry = NewsSentimentEntry(
                stock_symbol=article['stock'],
                date=datetime.now(),
                headline=article['headline'],
                sentiment=result['label'],
                score=result['score'],
            )
            if article['stock'] not in self.sentiment_history:
                self.sentiment_history[article['stock']] = []
            self.sentiment_history[article['stock']].append(entry)
