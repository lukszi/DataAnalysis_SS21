from retrieval.reddit.redditExtractor import RedditExtractor
from database.DatabaseController import DatabaseController
from retrieval.reddit.symbolExtractor import SymbolExtractor

symbol_extractor = SymbolExtractor("res/ticker.csv")
extractor = RedditExtractor(symbol_extractor)
database_controller = DatabaseController("res/RedditStocks.db")

results = extractor.extract_last_n_submissions(2)
for result in results:
    database_controller.add_reddit_post_from_model(result)
