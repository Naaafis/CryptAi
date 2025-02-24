from datetime import datetime
from typing import List, Dict
from tqdm import tqdm  
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
        self.sentiment_history: Dict[str, List[NewsSentimentEntry]] = {}
        self.sec_filing_history: Dict[str, List[dict]] = {}

    def monitor_news(self, stock_symbols: List[str]):
        """Fetch and analyze news sentiment for stock symbols."""
        print(f"Fetching and analyzing sentiment for {len(stock_symbols)} stocks...")

        for symbol in tqdm(stock_symbols, desc="Monitoring Stocks"):
            articles = self.data_source.fetch_news([symbol])

            if not articles:
                print(f"No news found for {symbol}")
                continue

            texts = [f"{article['headline']} {article['content']}" for article in articles]
            sentiment_results = self.analyzer.analyze(texts)

            for article, sentiment in zip(articles, sentiment_results):
                try:
                    date = datetime.fromtimestamp(article['date']) if article['date'] else datetime.now()
                except (ValueError, TypeError):
                    date = datetime.now()

                entry = NewsSentimentEntry(
                    stock_symbol=symbol,
                    date=date,
                    headline=article['headline'],
                    sentiment=sentiment['label'],
                    score=sentiment['score'],
                )

                if symbol not in self.sentiment_history:
                    self.sentiment_history[symbol] = []
                self.sentiment_history[symbol].append(entry)

        print("News monitoring complete.")

    def monitor_sec(self, stock_symbols: List[str], filing_type: List[str] = ["10-K", "10-Q", "8-K"], amount: int = 3):
        """Fetch SEC filings and store results for a list of stock symbols."""
        print(f"Fetching SEC filings for {len(stock_symbols)} stocks...")

        filings = self.data_source.fetch_sec(stock_symbols, amount=amount)

        for filing in filings:
            symbol = filing.get("ticker")  # ✅ Ensure we correctly reference "ticker"

            if not symbol:
                print("[SECMonitor] Warning: Missing ticker key in filing response.")
                continue

            form_type = filing["filing_type"]

            if form_type not in filing_type:
                print(f"[SECMonitor] Skipping {form_type} filing for {symbol}.")
                continue

            if symbol not in self.sec_filing_history:
                self.sec_filing_history[symbol] = []

            self.sec_filing_history[symbol].append(filing)

            # Trigger advanced analysis if relevant filing detected
            self.analyze_filing(filing)

        print("SEC filings monitoring complete.")


    def analyze_filing(self, filing: dict):
        """Process a filtered SEC filing and trigger deeper analysis."""
        print(f"[SECMonitor] Triggering advanced analysis for {filing['filing_type']} filing of {filing['ticker']}")

        # ✅ Send the filing sections to an AI agent for processing
        sections = filing.get("sections", {})
        for section_name, text in sections.items():
            print(f"[SECMonitor] Analyzing Section: {section_name} ({len(text)} characters)")

        # Here, we could pass sections to an AI pipeline for NLP summarization
        # For now, we print and store for further processing
