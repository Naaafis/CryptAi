from ...finnlp.finnlp.data_sources.news.seekingalpha_date_range import SeekingAlpha_Date_Range
from .base_news_fetcher import BaseNewsFetcher


class SeekingAlphaFetcher(BaseNewsFetcher):
    def __init__(self, start_date: str, end_date: str):
        """
        :param start_date: Start date for filtering articles (YYYY-MM-DD).
        :param end_date: End date for filtering articles (YYYY-MM-DD).
        """
        self.start_date = start_date
        self.end_date = end_date
        self.downloader = SeekingAlpha_Date_Range()

    def fetch(self, stock_symbol: str) -> list[dict]:
        """
        Fetch news articles from Seeking Alpha for a given stock symbol.

        :param stock_symbol: Stock ticker symbol (e.g., "AAPL").
        :return: List of dictionaries containing article details.
        """
        try:
            # ✅ Removed the incorrect `pages` argument
            self.downloader.download_date_range_stock(
                start_date=self.start_date,
                end_date=self.end_date,
                stock=stock_symbol
            )

            df = self.downloader.dataframe

            if df.empty:
                print(f"[SeekingAlphaFetcher] No news data found for {stock_symbol}.")
                return []

            articles = df.to_dict(orient="records")

            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'headline': article.get('title', ''),
                    'summary': '',
                    'date': article.get('publishOn', None),  # Seeking Alpha uses 'publishOn'
                    'url': '',  # No URL scraping yet
                    'source': "Seeking Alpha",
                })

            return formatted_articles

        except Exception as e:
            print(f"[SeekingAlphaFetcher] Error fetching news for {stock_symbol}: {e}")
            return []
