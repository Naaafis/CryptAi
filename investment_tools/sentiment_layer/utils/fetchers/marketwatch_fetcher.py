from ...finnlp.finnlp.data_sources.news.marketwatch_streaming import MarketWatch_Streaming
from .base_news_fetcher import BaseNewsFetcher


class MarketWatchFetcher(BaseNewsFetcher):
    def __init__(self, keyword: str = "stock market", start_date: str = None, end_date: str = None):
        """
        :param keyword: Search keyword for MarketWatch.
        :param start_date: Start date for filtering articles (YYYY-MM-DD).
        :param end_date: End date for filtering articles (YYYY-MM-DD).
        """
        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date
        self.downloader = MarketWatch_Streaming()

    def fetch(self, stock_symbol: str) -> list[dict]:
        """
        Fetch news articles from MarketWatch using a keyword search.

        :param stock_symbol: Stock ticker symbol (used as a keyword).
        :return: List of dictionaries containing article details.
        """
        try:
            self.downloader.download_date_range_search(
                start_date=self.start_date, 
                end_date=self.end_date, 
                keyword=stock_symbol
            )
            
            df = self.downloader.dataframe

            if df.empty:
                print(f"[MarketWatchFetcher] No news data found for {stock_symbol}.")
                return []

            articles = df.to_dict(orient="records")

            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'headline': article.get('title', ''),
                    'summary': '',
                    'date': article.get('time', None),
                    'url': '',  # No URL scraping yet
                    'source': "MarketWatch",
                })

            return formatted_articles

        except Exception as e:
            print(f"[MarketWatchFetcher] Error fetching news for {stock_symbol}: {e}")
            return []
