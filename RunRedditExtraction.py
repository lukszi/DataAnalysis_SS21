import time
from typing import Optional

from retrieval.reddit.redditExtractor import RedditExtractor
from database.DatabaseController import DatabaseController
from retrieval.reddit.symbolExtractor import SymbolExtractor
from datetime import datetime


symbol_extractor = SymbolExtractor("res/ticker.csv")
extractor = RedditExtractor(symbol_extractor)
database_controller = DatabaseController("res/RedditStocks.db")


def extract_and_safe_reddit_posts_in_database(last_n_submissions: int) -> None:
    """
    Extracts Reddit posts with RedditExtractor and saves Reddit post and mentioned Tickers in database
    :param last_n_submissions: Number of last n submission on Reddit
    :return: None
    """
    start_time = time.time()
    results = extractor.extract_last_n_submissions(last_n_submissions)
    print(time.time()-start_time)
    safe_reddit_posts_in_database(results)
    print(time.time() - start_time)

    print(f"{datetime.now()}: Starting looped extraction")
    extracted_items = len(results)
    loops_ran = 0
    sleep_time = 60
    while True:
        try:
            results = extractor.extract_up_to_last_submission()
            extracted_items += len(results)
            safe_reddit_posts_in_database(results)
            loops_ran += 1
            print(f"{datetime.now()}: Extracted {len(results)} items this cycle, sleeping {sleep_time} seconds")
            time.sleep(sleep_time)
        except InterruptedError:
            print(f"{datetime.now()}: Stopping extraction")
            break
    print(f"{datetime.now()}: finished extracting {extracted_items} mentions in {loops_ran} cycles")


def safe_reddit_posts_in_database(results):
    """
    Saves all stock mentions in the database
    :param results:
    :return:
    """
    interrupt: Optional[InterruptedError] = None
    for result in results:
        try:
            database_controller.add_stock_mention_to_database(result)
        except Exception as e:
            print(e)
            continue
        except InterruptedError as e:
            interrupt = e
            print("Got interrupt order, finish persisting extracted data")
            continue

    # Pass on interrupt exception
    if interrupt is not None:
        raise interrupt


extract_and_safe_reddit_posts_in_database(100)
