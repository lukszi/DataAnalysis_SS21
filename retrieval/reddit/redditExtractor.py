import json
from praw.models import Subreddit
from praw import Reddit

from DataAnalysis_SS21.retrieval.reddit.helper_methods import print_attrs
from retrieval.reddit.symbolExtractor import SymbolExtractor

config_path = "res/reddit_config.json"
if __name__ == '__main__':
    config_path = "../../res/reddit_config.json"


class RedditExtractor:
    __wsb: Subreddit
    __reddit: Reddit
    __symbol_extractor: SymbolExtractor
    __config: dict[str, str]

    def __init__(self):
        self.__load_config()
        self.__setup_reddit()
        self.__symbol_extractor = SymbolExtractor("ticker.csv")

    def extract_last_n_posts(self, n: int) -> None:
        wsb_new = self.__wsb.new(limit=n)
        for submission in wsb_new:
            print_attrs(submission,
                        ["title", "score", "permalink", "url", "is_video", "is_meta" "is_self", "self_text"])
            symbols = self.__symbol_extractor.extract_symbols(submission)
            print(f"Symbols:\t{symbols}")
            print("\n\n")

    def __load_config(self):
        with open(config_path, "r", encoding="UTF-8") as config_file:
            self.__config = json.load(config_file)

    def __setup_reddit(self):
        self.__reddit = Reddit(client_id=self.__config["client_id"], client_secret=self.__config["client_secret"],
                               password=self.__config["password"],
                               user_agent="android:com.example.myredditapp:v1.2.4",
                               username=self.__config["username"])
        self.__wsb = self.__reddit.subreddit("WallStreetBets")


if __name__ == '__main__':
    extr = RedditExtractor()
    extr.extract_last_n_posts(2)
