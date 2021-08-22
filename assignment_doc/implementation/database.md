# SQL-Alchemy database

The source files relevant to this discussion can be found [here](../../database).

## Scope

The Database part should save all information extracted from the reddit posts.
First in the [StockMention](../../database/Model/StockMention.py) to later commit it 
into the database. The data collected are:

* Reddit Post url
* Score
* Last time the score got updated
* Up votes of the post
* Down votes of the post
* Up-vote ratio
* Number of comments
* Datetime when the post was made
* Mentioned stocks
* ID as a primary key

## Implementation

We created a Database with [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) with 2 Tables. The database 
will be created automatically when starting the [RunRedditExtraction](../../RunRedditExtraction.py).

1. To collect all the generell data of the reddit post
2. The stocks mentioned in a post because some posts mentioned many stocks at once

We connected these two Tables over the ID of the post. 

In the [DatabaseController](../../database/DatabaseController.py) we implemented functions 
to add or remove one or many [StockMention](../../database/Model/StockMention.py) 
objects to the database.

## Issues

The setup and implementation of the database had various issues.

1. We hoped to create one Table with all the data until the point where we 
   found out that people mentioned many stocks in one post. So we had to add an 
   array of stock tokens. SQLAlchemy was not able to provide an easy way 
   to insert an array into a table. So we had to make another table with a 1 
   to n relation to capture all the stock tokens mentioned in a post.
   
   
2. Another problem occurred later on after some time of extracting 
   data from the reddit post the Reddit Api started to collect the 
   same posts over and over again but the post url which is unique 
   always throw an error when we tried to double add a post.
   So we had to catch the exception thrown every time the 
   [RedditExtractor](../../retrieval/reddit/redditExtractor.py)
   extracted a post we had already saved in the database.