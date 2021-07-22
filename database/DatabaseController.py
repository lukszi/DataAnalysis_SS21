from sqlalchemy.orm import sessionmaker
from typing import List
from database.Model.StockMention import StockMention, Stocks

from sqlalchemy import *
from pathlib import Path

from database.Model import Base

DATABASE_NAME = '../res/RedditStocks.db'


class DatabaseController:

    def __init__(self, database_path: str = DATABASE_NAME):
        """
        Creates a engine and a Session with the Database
        """
        create_database_if_not_exists(database_path)
        self.engine = create_engine(f'sqlite:///{database_path}')
        self.Session = sessionmaker(self.engine)

    def add_stock_mention_to_database(self, stock_mention: StockMention) -> None:
        """
        Adds a reddit post to the 'RedditStocks.db' database with all stocks mentioned.
        :param stock_mention: Model with data to be stored in Database
        """
        conn = self.engine.connect()
        with self.Session(bind=conn) as session:
            session.add(stock_mention)
            session.commit()

    def add_stocks_mention_to_database(self, stock_mentions) -> None:
        """
        Adds a list of reddit post to the 'RedditStocks.db' database with all stocks mentioned.
        :param stock_mentions: List if Models with data to be stored in Database
        :return:
        """
        conn = self.engine.connect()
        with self.Session(bind=conn) as session:
            for stock_mention in stock_mentions:
                session.add(stock_mention)
            session.commit()

    def get_stock_mention_from_database(self, stock_mention_id: int) -> List:
        """
        Gets a list tuples which contains the stock mentioned with the specific stock_mention_id
        and a stocktoken that was mentioned in the post
        :param stock_mention_id: the id of the mentioned stock post
        :return: a list of tuples (StockMention, stock_token)
        """
        conn = self.engine.connect()
        with self.Session(bind=conn) as session:
            result = session.query(StockMention, Stocks.stock_token)\
                .filter(StockMention.stock_mention_id == Stocks.stock_mention_id)\
                .filter(StockMention.stock_mention_id == stock_mention_id)\
                .all()
            return [row._data for row in result]

    def get_stocks_mention_from_database(self) -> List:
        """
        Gets a list tuples which contains all stocks mentioned out of the database
        and the stocktoken that was mentioned in the post
        :return: a list of tuples (StockMention, stock_token)
        """
        conn = self.engine.connect()
        with self.Session(bind=conn) as session:
            result = session.query(StockMention, Stocks.stock_token)\
                .filter(StockMention.stock_mention_id == Stocks.stock_mention_id)\
                .all()
            return [row._data for row in result]


def create_database_if_not_exists(database_path: str) -> None:
    """
    Creates the database if not exists
    """
    database = Path(database_path)
    if not database.is_file():
        engine = create_engine(f'sqlite:///{database_path}')
        Base.metadata.create_all(bind=engine)
    else:
        print('database already exists')


if __name__ == '__main__':
    database_controller = DatabaseController()
    stock_mention = database_controller.get_stock_mention_from_database(2)
    print(stock_mention)
    stock_mentions = database_controller.get_stocks_mention_from_database()
    print(stock_mentions)
