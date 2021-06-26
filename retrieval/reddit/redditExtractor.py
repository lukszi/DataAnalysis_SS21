import json
from datetime import datetime
from typing import List

from praw.models import Subreddit, Submission
from praw import Reddit

from DataAnalysis_SS21.retrieval.reddit.helper_methods import print_attrs
from retrieval.reddit.symbolExtractor import SymbolExtractor
from storage.Model import StockMention

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

    def extract_last_n_posts(self, n: int) -> List[StockMention]:
        parsed_posts: List[StockMention] = []
        wsb_new = self.__wsb.new(limit=n)
        for submission in wsb_new:
            tickers_in_submission = self.__symbol_extractor.extract_symbols(submission)
            if len(tickers_in_submission) == 0:
                continue

            mention = self.__create_model(submission, tickers_in_submission)
            parsed_posts.append(mention)
        return parsed_posts

    @staticmethod
    def __create_model(submission: Submission, tickers_in_submission: List[str]) -> StockMention:
        posted = datetime.fromtimestamp(submission.created_utc)
        mention = StockMention(submission.url, tickers_in_submission, posted, datetime.now(), submission.score,
                               submission.ups, submission.downs, submission.upvote_ratio, submission.num_comments)
        return mention

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
    extractor = RedditExtractor()
    results = extractor.extract_last_n_posts(2)
    print(results)
