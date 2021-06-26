from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from typing import List

from Database.RedditStocksTables import RedditPostsTable, StocksTable, DATABASE_NAME

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(engine)


def add_reddit_post(post_url: str, posted: datetime, votes_updated: datetime, stocks_token: List[str] = None):
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


if __name__ == '__main__':
    stocks = ['ASD', 'PAD']
    add_reddit_post('www.test.de', datetime.now(), datetime.now(), stocks)
