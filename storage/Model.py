from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class StockMention:
    post_url: str
    stocks: list[str]
    posted: datetime
    votes_updated: datetime
    votes: int
