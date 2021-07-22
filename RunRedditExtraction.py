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
    import time
    start_time = time.time()
    results = extractor.extract_last_n_submissions(last_n_submissions)
    print(time.time()-start_time)
    for result in results:
        try:
            database_controller.add_stock_mention_to_database(result)
        except:
            continue
    print(time.time() - start_time)


extract_and_safe_reddit_posts_in_database(25000)
