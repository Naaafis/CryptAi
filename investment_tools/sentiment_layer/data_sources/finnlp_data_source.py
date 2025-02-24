import os
import sys
from typing import List
from sentiment_layer.data_sources.base_data_sources import BaseDataSource
from sentiment_layer.utils.fetchers.base_news_fetcher import BaseNewsFetcher
from sentiment_layer.utils.fetchers.sec_fetcher import SECFetcher  # Import SEC fetcher


class FinNLPDataSource(BaseDataSource):
    def __init__(self, fetchers: List[BaseNewsFetcher], sec_fetcher: SECFetcher):
        """
        :param fetchers: List of fetchers implementing BaseNewsFetcher (e.g., CNBCFetcher)
        :param sec_fetcher: Fetcher instance for SEC filings.
        """
        finnlp_path = os.path.join(os.path.dirname(__file__), '../finnlp')
        if finnlp_path not in sys.path:
            sys.path.append(finnlp_path)

        self.fetchers = fetchers
        self.sec_fetcher = sec_fetcher  # New SEC fetcher instance

    def fetch_news(self, stock_symbols: List[str]) -> List[dict]:
        """
        Fetch news articles for a list of stock symbols.
        """
        articles = []
        for symbol in stock_symbols:
            for fetcher in self.fetchers:
                try:
                    fetched_articles = fetcher.fetch(symbol)
                    for article in fetched_articles:
                        articles.append({
                            'stock': symbol,
                            'headline': article.get('headline', ''),
                            'content': article.get('summary', ''),
                            'date': article.get('date', None),
                            'url': article.get('url', ''),
                            'source': article.get('source', ''),
                        })
                except Exception as e:
                    print(f"[FinNLPDataSource] Error fetching news for {symbol} from {fetcher.__class__.__name__}: {e}")

        return articles

    def fetch_sec(self, stock_symbols: List[str], filing_type: str = "10-K", amount: int = 3) -> List[dict]:
        """
        Fetch SEC filings for the given stock symbols.

        :param stock_symbols: List of stock ticker symbols (e.g., ["AAPL", "TSLA"])
        :param filing_type: SEC filing type ("10-K", "10-Q").
        :param amount: Number of filings to fetch.
        :return: List of SEC filings formatted as dicts.
        """
        filings = self.sec_fetcher.fetch()

        formatted_filings = []
        for filing in filings:
            formatted_filings.append({
                'ticker': filing["ticker"],
                'filing_type': filing["filing_type"],
                'filing_year': filing["filing_year"],
                'url': filing["filing_url"],
                'sections': filing["sections"],  # Full SEC document text in sections
            })

        return formatted_filings
