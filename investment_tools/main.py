from sentiment_layer.data_sources.finnlp_data_source import FinNLPDataSource
from sentiment_layer.analyzers.finbert_analyzer import FinBERTAnalyzer
from sentiment_layer.monitors.sentiment_monitor import SentimentMonitor

if __name__ == "__main__":
    data_source = FinNLPDataSource()
    analyzer = FinBERTAnalyzer()
    monitor = SentimentMonitor(data_source, analyzer)

    monitor.monitor(["AAPL", "TSLA"])
    print(monitor.sentiment_history)
