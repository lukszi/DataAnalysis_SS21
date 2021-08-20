import json
from datetime import datetime
from typing import List, Iterator, Optional, Dict

from praw.models import Subreddit, Submission
from praw import Reddit

from retrieval.reddit.symbolExtractor import SymbolExtractor
from database.Model.StockMention import StockMention

config_path = "res/reddit_config.json"
if __name__ == '__main__':
    config_path = "../../res/reddit_config.json"


class RedditExtractor:
    __wsb: Subreddit
    __reddit: Reddit
    __symbol_extractor: SymbolExtractor
    __config: Dict[str, str]
    __last_retrieved_post: str

    def __init__(self, symbol_extractor: SymbolExtractor):
        self.__load_config()
        self.__setup_reddit()
        self.__symbol_extractor = symbol_extractor

    def extract_up_to_last_submission(self) -> List[StockMention]:
        """
        Extracts a list of StockMentions from the newest submissions on reddit up to the last submission that has ben
        parsed already

        :return: List of all stockMentions found
        """
        wsb_new: Iterator[Submission] = self.__wsb.new()
        mentions_found: List[StockMention] = self.__extract_from_submissions(wsb_new, stop_at_last_submission=True)
        return mentions_found

    def extract_last_n_submissions(self, n: int) -> List[StockMention]:
        """
        Extracts a list of StockMentions from the n newest submissions on reddit
        :param n: number of submissions to be evaluated
        :return: List of all stockMentions found in the n last submissions
        """
        wsb_new: Iterator[Submission] = self.__wsb.new(limit=n)
        return self.__extract_from_submissions(wsb_new)

    def __extract_from_submissions(self, submissions: Iterator[Submission], stop_at_last_submission: bool = False) -> \
            List[StockMention]:
        """
        From an Iterator over submissions extracts all stocks mentioned

        :param submissions: Submissions to be evaluated
        :return: List of stockMentions that can be saved into the database
        """

        # TODO: Logic to stop if I get an infinite iterator
        parsed_posts: List[StockMention] = []
        first_submission: Optional[str] = None

        for i, submission in enumerate(submissions):
            # Logic to continue up to last parsed submission
            if first_submission is None:
                first_submission = submission.url
            # Stop at submission that was previously found
            if stop_at_last_submission and self.__last_retrieved_post is not None:
                if submission.url == self.__last_retrieved_post:
                    break

            # Skip unparsable posts
            if not self.__submission_is_parsable(submission):
                continue

            mention = self.__extract_from_submission(submission)
            if mention is not None:
                parsed_posts.append(mention)

        self.__last_retrieved_post = first_submission
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
        return RedditExtractor.__create_model_object(submission, tickers_in_submission)

    @staticmethod
    def __create_model_object(submission: Submission, tickers_in_submission: List[str]) -> StockMention:
        posted = datetime.fromtimestamp(submission.created_utc)
        mention = StockMention(post_url=submission.url,
                               score_updated=datetime.now(),
                               score=submission.score,
                               up_votes=submission.ups,
                               down_votes=submission.downs,
                               upvote_ratio=submission.upvote_ratio,
                               num_comments=submission.num_comments,
                               posted=posted,
                               stocks=tickers_in_submission)
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

    @staticmethod
    def __submission_is_parsable(submission):
        return submission.is_self


if __name__ == '__main__':
    smbl_xtrct = SymbolExtractor("../../res/ticker.csv")
    extractor = RedditExtractor(smbl_xtrct)
    results = extractor.extract_last_n_submissions(2)
    print(results)
