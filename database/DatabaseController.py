from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from typing import List

from database.RedditStocksTables import RedditPostsTable, StocksTable, DATABASE_NAME
from storage import Model

class DatabaseController:

    engine = create_engine(f'sqlite:///{DATABASE_NAME}')
    Session = sessionmaker(engine)


    def add_reddit_post(post_url: str, posted: datetime, votes_updated: datetime, stocks_token: List[str] = None):
        """
        Adds a reddit post to the 'RedditStocks.db' database with all stocks mentioned.
        :param post_url: reddit post url
        :param posted: reddit post creation date
        :param votes_updated: last time reddit votes got updated
        :param stocks_token: a list of all stock tokens mentioned in the reddit post
        """
        conn = engine.connect()
        with Session(bind=conn) as session:
            reddit_post = RedditPostsTable(post_url=post_url,
                                           posted=posted,
                                           votes_updated=votes_updated)
            if stocks_token is not None:
                for token in stocks_token:
                    exists = session.query(session.query(StocksTable).filter_by(token=token).exists()).scalar()
                    if not exists:
                        stock = StocksTable(token=token)
                        reddit_post.stocks.append(stock)
            session.add(reddit_post)
            session.commit()


    def add_reddit_post_from_model(model: Model):
        """
        Adds a reddit post to the 'RedditStocks.db' database with all stocks mentioned.
        :param model: Model with all data necessary to execute add_reddit_post with shared arguments
        """
        add_reddit_post(model.post_url, model.posted, model.votes_updated, model.stocks)


if __name__ == '__main__':
    stocks = ['ASD', 'PAD']
    add_reddit_post('www.test.de', datetime.now(), datetime.now(), stocks)
