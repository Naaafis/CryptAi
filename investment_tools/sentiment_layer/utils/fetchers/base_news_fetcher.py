from abc import ABC, abstractmethod
from typing import List


class BaseNewsFetcher(ABC):
    @abstractmethod
    def fetch(self, stock_symbol: str) -> List[dict]:
        """
        Fetches news articles for a given stock symbol.
        Each dictionary in the returned list should contain:
        - 'title': str
        - 'summary': str
        - 'datetime': epoch timestamp (int) or None
        - 'url': str
        - 'source': str
        """
        pass
