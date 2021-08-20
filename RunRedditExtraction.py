import time
from typing import Optional

from prawcore import ServerError
from sqlalchemy.exc import IntegrityError

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
    num_extracted_items = len(results)
    loops_ran = 0
    sleep_time = 60
    while True:
        try:
            results = extractor.extract_up_to_last_submission()
            num_extracted_items += len(results)
            safe_reddit_posts_in_database(results)
            loops_ran += 1
            print(f"{datetime.now()}: Extracted {len(results)} items this cycle, sleeping {sleep_time} seconds")
            time.sleep(sleep_time)
        except InterruptedError:
            print(f"{datetime.now()}: Stopping extraction")
            break
        except ServerError as e:
            print(e)

    print(f"{datetime.now()}: finished extracting {num_extracted_items} mentions in {loops_ran} cycles")


def safe_reddit_posts_in_database(results):
    """
    Saves all stock mentions in the database
    :param results:
    :return:
    """
    interrupt: Optional[InterruptedError] = None
    num_inserted = 0
    num_insertion_failed = 0
    for result in results:
        try:
            database_controller.add_stock_mention_to_database(result)
            num_inserted += 1
        except IntegrityError:
            num_insertion_failed += 1
        except Exception as e:
            print(e)
        except InterruptedError as e:
            interrupt = e
            print("Got interrupt order, finish persisting extracted data")

    print(f"{datetime.now()}: inserted/failed: {num_inserted}/{num_insertion_failed}")
    # Pass on interrupt exception
    if interrupt is not None:
        raise interrupt


extract_and_safe_reddit_posts_in_database(250)
