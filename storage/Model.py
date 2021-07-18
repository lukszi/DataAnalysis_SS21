from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from typing import List
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pathlib import Path

from database.RedditStocksTables import Base


@dataclass_json
@dataclass
class StockMention(Base):
    """
        Table with all reddit submissions
        """
    __tablename__ = 'StockMention'

    post_url: str = Column(String)
    score_updated: datetime = Column(DATETIME)
    score: int = Column(Integer)
    up_votes: int = Column(Integer)
    down_votes: int = Column(Integer)
    upvote_ratio: float = Column(Float)
    num_comments: int = Column(Integer)
    posted: datetime = Column(DATETIME)
    stocks: List[str] = Column(List[str])
