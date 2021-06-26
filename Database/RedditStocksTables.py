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
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    post_url = Column(String)
    posted = Column(DATETIME)
    votes_updated = Column(DATETIME)
    stocks = relationship("StocksTable",
                          secondary=reddit_posts_stocks_association_table)


class StocksTable(Base):
    __tablename__ = 'stocks'

    token = Column(String(4), primary_key=True)


def create_database_if_not_exists():
    database = Path(DATABASE_NAME)
    if not database.is_file():
        engine = create_engine(f'sqlite:///{DATABASE_NAME}')
        Base.metadata.create_all(bind=engine)
    else:
        print('Database already exists')


if __name__ == "__main__":
    create_database_if_not_exists()
