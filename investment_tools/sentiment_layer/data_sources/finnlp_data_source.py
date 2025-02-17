import os
import sys
from typing import List
from sentiment_layer.data_sources.base_data_sources import BaseDataSource
from sentiment_layer.utils.fetchers.base_news_fetcher import BaseNewsFetcher


class FinNLPDataSource(BaseDataSource):
    def __init__(self, fetcher: BaseNewsFetcher):
        """
        :param fetcher: Any class that implements BaseNewsFetcher
        """
        finnlp_path = os.path.join(os.path.dirname(__file__), '../finnlp')
        if finnlp_path not in sys.path:
            sys.path.append(finnlp_path)

        self.fetcher = fetcher

    def fetch_news(self, stock_symbols: List[str]) -> List[dict]:
        articles = []
        for symbol in stock_symbols:
            try:
                fetched_articles = self.fetcher.fetch(symbol)

                for article in fetched_articles:
                    articles.append({
                        'stock': symbol,
                        'headline': article.get('title', ''),
                        'content': article.get('summary', ''),
                        'date': article.get('datetime', None),  # Epoch timestamp
                        'url': article.get('url', ''),
                        'source': article.get('source', ''),
                    })

            except Exception as e:
                print(f"[FinNLPDataSource] Error fetching news for {symbol}: {e}")

        return articles
