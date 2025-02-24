from ...finnlp.finnlp.data_sources.news.cnbc_streaming import CNBC_Streaming
from .base_news_fetcher import BaseNewsFetcher


class CNBCFetcher(BaseNewsFetcher):
    def __init__(self, keyword: str = "stock market", rounds: int = 3, delay: float = 0.5):
        """
        :param keyword: Search keyword for CNBC articles.
        :param rounds: Number of search result pages to fetch.
        :param delay: Delay between API calls to prevent rate limiting.
        """
        self.keyword = keyword
        self.rounds = rounds
        self.delay = delay
        self.downloader = CNBC_Streaming()

    def fetch(self, stock_symbol: str) -> list[dict]:
        """
        Fetch news articles from CNBC for a given stock symbol.

        :param stock_symbol: Stock ticker symbol (used as a keyword for CNBC search).
        :return: List of dictionaries containing article details.
        """
        try:
            # ✅ Using CNBC’s search function instead of a stock-specific API
            self.downloader.download_streaming_search(keyword=stock_symbol, rounds=self.rounds, delay=self.delay)
            
            df = self.downloader.dataframe

            if df.empty:
                print(f"[CNBCFetcher] No news data found for {stock_symbol}.")
                return []

        
            articles = df.to_dict(orient="records")

            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'headline': article.get('cn:title', ''),  # Using cn:title for the headline
                    'summary': article.get('description', ''),
                    'date': article.get('datePublished', None),
                    'url': article.get('url', ''),  # Using 'url' instead of 'link'
                    'source': "CNBC",
                })

            return formatted_articles

        except Exception as e:
            print(f"[CNBCFetcher] Error fetching news for {stock_symbol}: {e}")
            return []
