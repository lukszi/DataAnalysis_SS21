from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from typing import List
from sqlalchemy import *
from sqlalchemy.orm import relationship

from database.Model import Base


@dataclass_json
@dataclass
class StockMention(Base):
    """
    Table with all reddit submissions
    """
    __tablename__ = 'StockMention'

    stock_mention_id: int = Column(Integer, primary_key=True, autoincrement=True)
    post_url: str = Column(String, unique=True)
    score_updated: datetime = Column(DATETIME)
    score: int = Column(Integer)
    up_votes: int = Column(Integer)
    down_votes: int = Column(Integer)
    upvote_ratio: float = Column(Float)
    num_comments: int = Column(Integer)
    posted: datetime = Column(DATETIME)
    stocks = relationship('Stocks', backref='person', lazy='dynamic')

    def __init__(self, post_url: str, score_updated: datetime, score: int, up_votes: int,
                 down_votes: int, upvote_ratio: float, num_comments: int, posted: datetime, stocks: List[str]):
        self.post_url = post_url
        self.score_updated = score_updated
        self.score = score
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.upvote_ratio = upvote_ratio
        self.num_comments = num_comments
        self.posted = posted
        for stock in stocks:
            stock_col = Stocks(stock)
            self.stocks.append(stock_col)


class Stocks(Base):
    __tablename__ = 'Stocks'

    stocks_id: int = Column(Integer, primary_key=True, autoincrement=True)
    stock_mention_id: int = Column(Integer, ForeignKey('StockMention.stock_mention_id'), nullable=False)
    stock_token: str = Column(String)

    def __init__(self, stock_token: str):
        self.stock_token = stock_token

