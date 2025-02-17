import sys
import os

# Add FinNLP submodule to the path
finnlp_path = os.path.join(os.path.dirname(__file__), 'sentiment_layer', 'finnlp')
if finnlp_path not in sys.path:
    sys.path.append(finnlp_path)

from sentiment_layer.data_sources.finnlp_data_source import FinNLPDataSource
from sentiment_layer.analyzers.finbert_analyzer import FinBERTAnalyzer
from sentiment_layer.monitors.sentiment_monitor import SentimentMonitor
from sentiment_layer.utils.fetchers.yahoo_news_fetcher import YahooNewsFetcher

api_key = os.getenv("FINNHUB_API_KEY")
if not api_key:
    raise ValueError("FINNHUB_API_KEY is not set in the environment.")

if __name__ == "__main__":
    finnhub_token = api_key # Go to  https://finnhub.io/dashboard
    yahoo_fetcher = YahooNewsFetcher(
        token=finnhub_token,
        start_date="2024-01-01",
        end_date="2024-02-20",
        stock_symbol="AAPL"
    )

    data_source = FinNLPDataSource(yahoo_fetcher)
    analyzer = FinBERTAnalyzer()
    monitor = SentimentMonitor(data_source, analyzer)

    monitor.monitor(["AAPL", "TSLA"])

    for symbol, entries in monitor.sentiment_history.items():
        print(f"\nSentiment History for {symbol}:")
        for entry in entries:
            print(entry)