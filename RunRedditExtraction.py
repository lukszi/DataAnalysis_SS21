from retrieval.reddit.redditExtractor import RedditExtractor
from database.DatabaseController import DatabaseController
from retrieval.reddit.symbolExtractor import SymbolExtractor


def extract_and_safe_reddit_posts_in_database(last_n_submissions: int) -> None:
    """
    Extracts Reddit posts with RedditExtractor and saves Reddit post and mentioned Tickers in database
    :param last_n_submissions: Number of last n submission on Reddit
    :return: None
    """
    symbol_extractor = SymbolExtractor("res/ticker.csv")
    extractor = RedditExtractor(symbol_extractor)
    database_controller = DatabaseController("res/RedditStocks.db")

    results = extractor.extract_last_n_submissions(last_n_submissions)
    for result in results:
        database_controller.add_reddit_post_from_model(result)


extract_and_safe_reddit_posts_in_database(10)
