from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pathlib import Path

Base = declarative_base()

DATABASE_NAME = '../res/RedditStocks.db'

reddit_posts_stocks_association_table = Table('RedditPostsStocksAssociation', Base.metadata,
                                              Column('reddit_posts_id', Integer, ForeignKey('reddit_posts.id')),
                                              Column('stocks_token', String, ForeignKey('stocks.token'))
                                              )


class RedditPostsTable(Base):
    """
    Table with all reddit posts
    """
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    post_url = Column(String)
    posted = Column(DATETIME)
    score_updated = Column(DATETIME)
    score = Column(Integer)
    up_votes = Column(Integer)
    down_votes = Column(Integer)
    upvote_ratio = Column(Float)
    num_comments = Column(Integer)
    stocks = relationship("StocksTable",
                          secondary=reddit_posts_stocks_association_table)


class StocksTable(Base):
    """
    Table with all stock tokens
    """
    __tablename__ = 'stocks'

    token = Column(String(4), primary_key=True)


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


if __name__ == "__main__":
    create_database_if_not_exists()
