from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pathlib import Path

Base = declarative_base()

DATABASE_NAME = '../res/RedditStocks.db'
#
#
# class StocksTable(Base):
#     """
#     Table with all stock tokens
#     """
#     __tablename__ = 'stocks'
#
#     token = Column(String(4), primary_key=True)


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
