from pydantic import BaseModel
from datetime import datetime

class NewsSentimentEntry(BaseModel):
    stock_symbol: str
    date: datetime
    headline: str
    sentiment: str
    score: float
