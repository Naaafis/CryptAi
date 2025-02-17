from ...finnlp.finnlp.data_sources.news.yahoo_streaming import Yahoo_Date_Range
from .base_news_fetcher import BaseNewsFetcher


class YahooNewsFetcher(BaseNewsFetcher):
    def __init__(self, token: str, start_date: str, end_date: str, stock_symbol: str):
        """
        :param token: Finnhub API token.
        :param start_date: Start date for news in YYYY-MM-DD format.
        :param end_date: End date for news in YYYY-MM-DD format.
        :param stock_symbol: Stock ticker symbol.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.stock_symbol = stock_symbol
        self.downloader = Yahoo_Date_Range(args={"token": token})

    def fetch(self, stock_symbol: str) -> list[dict]:
        try:
            self.downloader.download_date_range_stock(
                start_date=self.start_date,
                end_date=self.end_date,
                stock=stock_symbol
            )

            df = self.downloader.dataframe

            # Handle case where Finnhub API returns nothing
            if df.empty:
                print(f"[YahooNewsFetcher] No news data returned for {stock_symbol}")
                return []

            # Safeguard in case 'datetime' column is missing
            if 'datetime' not in df.columns:
                print(f"[YahooNewsFetcher] Missing 'datetime' column for {stock_symbol}, possible empty result set.")
                return []

            # Convert DataFrame into list of dictionaries
            articles = df.to_dict(orient='records')

            # Standardize fields
            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    'headline': article.get('headline', article.get('title', '')),
                    'summary': article.get('summary', ''),
                    'date': article.get('datetime', None),  # Epoch timestamp
                    'url': article.get('url', ''),
                    'source': article.get('source', 'Yahoo'),
                })

            return formatted_articles

        except Exception as e:
            print(f"[YahooNewsFetcher] Failed to fetch news for {stock_symbol}: {e}")
            return []
