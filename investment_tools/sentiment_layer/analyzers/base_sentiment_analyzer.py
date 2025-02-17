from typing import List
from abc import ABC, abstractmethod

class BaseSentimentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, texts: List[str]) -> List[dict]:
        """
        Takes a list of news headlines/articles and returns sentiment scores.
        """
        pass
