from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class StockMention:
    post_url: str
    stocks: List[str]
    posted: datetime
    score_updated: datetime
    score: int
    up_votes: int
    down_votes: int
    upvote_ratio: float
    num_comments: int
