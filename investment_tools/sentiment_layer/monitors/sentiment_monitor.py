from datetime import datetime
from typing import List, Dict
from tqdm import tqdm  # For progress bar
from sentiment_layer.analyzers.base_sentiment_analyzer import BaseSentimentAnalyzer
from sentiment_layer.utils.sentiment_models import NewsSentimentEntry
from sentiment_layer.data_sources.base_data_sources import BaseDataSource


class SentimentMonitor:
    def __init__(self, data_source: BaseDataSource, analyzer: BaseSentimentAnalyzer):
        """
        Initialize SentimentMonitor with a data source and a sentiment analyzer.

        :param data_source: Instance of BaseDataSource (e.g., FinNLPDataSource)
        :param analyzer: Instance of BaseSentimentAnalyzer (e.g., FinBERTAnalyzer)
        """
        self.data_source = data_source
        self.analyzer = analyzer
        # Store historical sentiment entries for each stock
        self.sentiment_history: Dict[str, List[NewsSentimentEntry]] = {}

    def monitor(self, stock_symbols: List[str]):
        """
        Fetch news, analyze sentiment, and store results for a list of stock symbols.

        :param stock_symbols: List of stock ticker symbols (e.g., ["AAPL", "TSLA"])
        """
        print(f"Fetching and analyzing news sentiment for {len(stock_symbols)} stocks...")
        
        # Display progress bar for the list of stocks
        for symbol in tqdm(stock_symbols, desc="Monitoring Stocks"):
            # Fetch news articles for the stock symbol from the data source
            articles = self.data_source.fetch_news([symbol])

            if not articles:
                print(f"No news found for {symbol}")
                continue

            # Extract headlines to feed into the sentiment analyzer
            texts = [article['headline'] for article in articles]

            # Analyze sentiment of all headlines in batch
            sentiment_results = self.analyzer.analyze(texts)

            # Loop through articles and sentiment results together
            for article, sentiment in zip(articles, sentiment_results):
                # Handle timestamps: Convert from epoch to datetime, or fallback to current time
                try:
                    date = datetime.fromtimestamp(article['date']) if article['date'] else datetime.now()
                except (ValueError, TypeError):
                    date = datetime.now()

                # Create a sentiment entry using Pydantic model
                entry = NewsSentimentEntry(
                    stock_symbol=symbol,
                    date=date,
                    headline=article['headline'],
                    sentiment=sentiment['label'],
                    score=sentiment['score'],
                )

                # Store the sentiment entry in the sentiment history
                if symbol not in self.sentiment_history:
                    self.sentiment_history[symbol] = []
                self.sentiment_history[symbol].append(entry)

        print("Monitoring complete.")
