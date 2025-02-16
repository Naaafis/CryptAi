from typing import List

class BaseDataSource(ABC):
    @abstractmethod
    def fetch_news(self, stock_symbols: List[str]) -> List[dict]:
        """
        Fetch news articles for a list of stock symbols.
        Returns a list of dicts with keys like 'stock', 'headline', 'content', 'date', etc.
        """
        pass
