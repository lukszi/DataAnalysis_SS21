import json
from datetime import datetime
from typing import List, Iterator, Optional

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

    def extract_last_n_submissions(self, n: int) -> List[StockMention]:
        """
        Extracts a list of StockMentions from the n newest submissions on reddit
        :param n: number of submissions to be evaluated
        :return: List of all stockMentions found in the n last submissions
        """
        wsb_new = self.__wsb.new(limit=n)
        return self.__extract_from_submissions(wsb_new)

    def __extract_from_submissions(self, submissions: Iterator[Submission]) -> List[StockMention]:
        """
        From an Iterator over submissions extracts all stocks mentioned

        :param submissions: Submissions to be evaluated
        :return: List of stockMentions that can be saved into the database
        """
        parsed_posts: List[StockMention] = []
        for submission in submissions:
            mention = self.__extract_from_submission(submission)
            if mention is not None:
                parsed_posts.append(mention)
        return parsed_posts

    def __extract_from_submission(self, submission: Submission) -> Optional[StockMention]:
        """
        Extracts a stockMention from a single submission

        :param submission: Submission to be evaluated
        :return: None if no tickers were found, otherwise a stockMention object is returned
        """
        tickers_in_submission = self.__symbol_extractor.extract_symbols(submission)
        if len(tickers_in_submission) == 0:
            return None
        return self.__create_model_object(submission, tickers_in_submission)

    @staticmethod
    def __create_model_object(submission: Submission, tickers_in_submission: List[str]) -> StockMention:
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
    results = extractor.extract_last_n_submissions(2)
    print(results)
