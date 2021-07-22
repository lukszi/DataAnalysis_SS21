from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from typing import List
from database.Model import StockMention

from sqlalchemy import *
from pathlib import Path

from database.Model import Base

DATABASE_NAME = '../res/RedditStocks.db'


class DatabaseController:

    def __init__(self, database_path: str = DATABASE_NAME):
        """
        Creates a engine and a Session with the Database
        """
        create_database_if_not_exists()
        self.engine = create_engine(f'sqlite:///{database_path}')
        self.Session = sessionmaker(self.engine)

    def add_reddit_post_from_model(self, stock_mention: StockMention) -> None:
        """
        Adds a reddit post to the 'RedditStocks.db' database with all stocks mentioned.
        :param stock_mention: Model with data to bne stored in Database
        """
        post_url: str = stock_mention.post_url
        stocks_token: List[str] = stock_mention.stocks
        posted: datetime = stock_mention.posted
        score_updated: datetime = stock_mention.score_updated
        score: int = stock_mention.score
        up_votes: int = stock_mention.up_votes
        down_votes: int = stock_mention.down_votes
        upvote_ratio: float = stock_mention.upvote_ratio
        num_comments: int = stock_mention.num_comments

        conn = self.engine.connect()
        with self.Session(bind=conn) as session:
            # reddit_post = RedditPostsTable(post_url=post_url,
            #                                posted=posted,
            #                                score_updated=score_updated,
            #                                score=score,
            #                                up_votes=up_votes,
            #                                down_votes=down_votes,
            #                                upvote_ratio=upvote_ratio,
            #                                num_comments=num_comments)
            # if stocks_token is not None:
            #     for token in stocks_token:
            #         exists = session.query(session.query(StocksTable).filter_by(token=token).exists()).scalar()
            #         if not exists:
            #             stock = StocksTable(token=token)
            #             reddit_post.stocks.append(stock)
            # session.add(reddit_post)
            session.commit()


def create_database_if_not_exists() -> None:
    """
    Creates the database if not exists
    """
    database = Path(DATABASE_NAME)
    if not database.is_file():
        engine = create_engine(f'sqlite:///{DATABASE_NAME}')
        Base.metadata.create_all(bind=engine)
    else:
        print('database already exists')


if __name__ == '__main__':
    create_database_if_not_exists()
    # stocks = ['TEST', 'HEY']
    # model = StockMention(post_url='www.test.de',
    #                      stocks=stocks,
    #                      posted=datetime.now(),
    #                      score_updated=datetime.now(),
    #                      score=2,
    #                      up_votes=5,
    #                      down_votes=3,
    #                      upvote_ratio=0.6,
    #                      num_comments=6)
    # dbc = DatabaseController()
    # dbc.add_reddit_post_from_model(model)
