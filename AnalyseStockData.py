from database.DatabaseController import DatabaseController
from retrieval import Financial


def analyse_something():
    database_controller = DatabaseController("res/RedditStocks.db")
    stocks_mention = database_controller.get_stocks_mention_from_database()
    for (stock_mention, stock_token) in stocks_mention:
        slopes = Financial.average_slopes_of_stock(stock_token, stock_mention.posted)
        print(slopes)


if __name__ == '__main__':
    analyse_something()
