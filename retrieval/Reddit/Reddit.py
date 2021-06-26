import json
from praw.models import Subreddit
from praw import Reddit

from DataAnalysis_SS21.retrieval.Reddit.helper import print_attrs
from retrieval.Reddit.stock_extraction import SymbolExtractor

config_path = "res/reddit_config.json"
if __name__ == '__main__':
    config_path = "../../res/reddit_config.json"


class RedditExtractor:
    wsb: Subreddit
    reddit: Reddit
    symbol_extractor: SymbolExtractor
    __config: dict[str, str]

    def __init__(self):
        self.load_config()
        self.setup_reddit()
        self.symbol_extractor = SymbolExtractor("ticker.csv")

    def extract_last_n_posts(self, n: int) -> None:
        wsb_new = self.wsb.new(limit=n)
        for submission in wsb_new:
            print_attrs(submission,
                        ["title", "score", "permalink", "url", "is_video", "is_meta" "is_self", "self_text"])
            symbols = self.symbol_extractor.extract_symbols(submission)
            print(f"Symbols:\t{symbols}")
            print("\n\n")

    def load_config(self):
        with open(config_path, "r", encoding="UTF-8") as config_file:
            self.__config = json.load(config_file)

    def setup_reddit(self):
        self.reddit = Reddit(client_id=self.__config["client_id"], client_secret=self.__config["client_secret"],
                             password=self.__config["password"],
                             user_agent="android:com.example.myredditapp:v1.2.4",
                             username=self.__config["username"])
        self.wsb = self.reddit.subreddit("WallStreetBets")
