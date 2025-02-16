from typing import List

class BaseSentimentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, texts: List[str]) -> List[dict]:
        """
        Takes a list of news headlines/articles and returns sentiment scores.
        """
        pass
