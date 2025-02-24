import sys
import os
from dotenv import load_dotenv

# Ensure FinNLP submodule is in the Python path
finnlp_path = os.path.join(os.path.dirname(__file__), 'sentiment_layer', 'finnlp')
if finnlp_path not in sys.path:
    sys.path.append(finnlp_path)

# Import necessary modules
from sentiment_layer.data_sources.finnlp_data_source import FinNLPDataSource
from sentiment_layer.analyzers.finbert_analyzer import FinBERTAnalyzer
from sentiment_layer.monitors.sentiment_monitor import SentimentMonitor

# Import Fetchers
from sentiment_layer.utils.fetchers.yahoo_news_fetcher import YahooNewsFetcher
from sentiment_layer.utils.fetchers.cnbc_fetcher import CNBCFetcher  
from sentiment_layer.utils.fetchers.sec_fetcher import SECFetcher  

# Load API key from `.env`
load_dotenv()
api_key = os.getenv("FINNHUB_API_KEY")
if not api_key:
    raise ValueError("FINNHUB_API_KEY is not set in the environment.")

if __name__ == "__main__":
    print("Initializing Sentiment & SEC Monitoring...")

    finnhub_token = api_key  

    # Stock Symbols for Testing
    stock_symbols = ["AAPL", "TSLA"]

    # Initialize News Fetchers
    print("Setting up news fetchers...")
    yahoo_fetcher = YahooNewsFetcher(token=finnhub_token, start_date="2025-02-01", end_date="2025-02-16")
    cnbc_fetcher = CNBCFetcher(rounds=3)

    # Initialize SEC Fetcher
    print("Setting up SEC fetcher...")
    sec_fetcher = SECFetcher(tickers=stock_symbols, filing_type="10-K", amount=2)

    # Create Data Source with Fetchers
    data_source = FinNLPDataSource(fetchers=[yahoo_fetcher, cnbc_fetcher], sec_fetcher=sec_fetcher)

    # Initialize Sentiment Analyzer
    analyzer = FinBERTAnalyzer()

    # Initialize Sentiment Monitor
    monitor = SentimentMonitor(data_source, analyzer)

    # Run SEC Filings Monitoring with Filtered Filings (10-K, 10-Q, 8-K)
    print("\nFetching SEC filings for stocks...\n")
    monitor.monitor_sec(stock_symbols, filing_type=["10-K", "10-Q", "8-K"], amount=2)

    # Display SEC Filings Results
    print("\nSEC Filings Summary:")
    for symbol, filings in monitor.sec_filing_history.items():
        print(f"\nSEC Filings for {symbol}:")
        for filing in filings[:3]:  # Show first 3 filings per stock
            print(f"Year: {filing['filing_year']}, Type: {filing['filing_type']}, URL: {filing['filing_url']}")

    print("\nSEC Filings monitoring complete.")


# import sys
# import os
# from dotenv import load_dotenv

# # ✅ Ensure FinNLP submodule is in the Python path
# finnlp_path = os.path.join(os.path.dirname(__file__), 'sentiment_layer', 'finnlp')
# if finnlp_path not in sys.path:
#     sys.path.append(finnlp_path)

# # ✅ Import necessary modules
# from sentiment_layer.data_sources.finnlp_data_source import FinNLPDataSource
# from sentiment_layer.analyzers.finbert_analyzer import FinBERTAnalyzer
# from sentiment_layer.monitors.sentiment_monitor import SentimentMonitor

# # ✅ Import Fetchers
# from sentiment_layer.utils.fetchers.yahoo_news_fetcher import YahooNewsFetcher
# from sentiment_layer.utils.fetchers.cnbc_fetcher import CNBCFetcher  
# from sentiment_layer.utils.fetchers.sec_fetcher import SECFetcher  # ✅ Added SEC Fetcher

# # ✅ Load API key from `.env`
# load_dotenv()
# api_key = os.getenv("FINNHUB_API_KEY")
# if not api_key:
#     raise ValueError("FINNHUB_API_KEY is not set in the environment.")

# if __name__ == "__main__":
#     print("🔹 Initializing Sentiment & SEC Monitoring...")

#     finnhub_token = api_key  # Go to https://finnhub.io/dashboard

#     # ✅ **Stock Symbols for Testing**
#     stock_symbols = ["AAPL", "TSLA"]  # Add more if needed

#     # ✅ **Initialize News Fetchers**
#     print("🔹 Setting up news fetchers...")
#     yahoo_fetcher = YahooNewsFetcher(token=finnhub_token, start_date="2025-02-01", end_date="2025-02-16")
#     cnbc_fetcher = CNBCFetcher(rounds=3)  

#     # ✅ **Initialize SEC Fetcher**
#     print("🔹 Setting up SEC fetcher...")
#     sec_fetcher = SECFetcher(tickers=stock_symbols, filing_type="10-K", amount=2)  # Fetch latest 10-K filings

#     # ✅ **Create Data Source with Fetchers**
#     data_source = FinNLPDataSource(fetchers=[yahoo_fetcher, cnbc_fetcher], sec_fetcher=sec_fetcher)

#     # ✅ **Initialize Sentiment Analyzer**
#     analyzer = FinBERTAnalyzer()

#     # ✅ **Initialize Sentiment Monitor**
#     monitor = SentimentMonitor(data_source, analyzer)

#     # ✅ **Run News Sentiment Monitoring**
#     # print(f"🔹 Fetching and analyzing sentiment for {len(stock_symbols)} stocks...\n")
#     # monitor.monitor_news(stock_symbols)

#     # # ✅ **Display Sentiment Results**
#     # for symbol, entries in monitor.sentiment_history.items():
#     #     print(f"\n🔹 Sentiment History for {symbol}:")
#     #     for entry in entries[:5]:  # Show first 5 entries per stock for readability
#     #         print(f"📰 {entry.date}: [{entry.sentiment}] {entry.headline}")

#     # print("\n✅ Sentiment monitoring complete.")

#     # ✅ **Run SEC Filings Monitoring**
#     print("\n🔹 Fetching SEC filings for stocks...\n")
#     monitor.monitor_sec(stock_symbols, filing_type="10-K", amount=2)

#     # ✅ **Display SEC Filings Results**
#     for symbol, filings in monitor.sec_filing_history.items():
#         print(f"\n🔹 SEC Filings for {symbol}:")
#         for filing in filings[:3]:  # Show first 3 filings per stock
#             print(f"📄 Year: {filing['filing_year']}, Type: {filing['filing_type']}, URL: {filing['url']}")

#     print("\n✅ SEC Filings monitoring complete.")
