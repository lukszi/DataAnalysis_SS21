# Reddit extraction

The source files relevant to this discussion can be found [here](../../retrieval/reddit).

## Scope
The Reddit extractor solves two problems:
* extracting relevant posts from the WallStreetBets subreddit 
* Search for relevant stocks in the extracted posts

## Implementation
Since it solves two problems, the implementation is split into the following two classes:
1. [redditExtractor](../../retrieval/reddit/redditExtractor.py)
1. [symbolExtractor](../../retrieval/reddit/symbolExtractor.py)

### redditExtractor.py
The reddit extractor uses the [PRAW](https://praw.readthedocs.io/en/stable/) library to fetch a given amount of posts
from the new section of WallStreetBets.

Each post then provided it is a "selfpost" - a post consisting largely of text - handed over to the [symbolExtractor](../../retrieval/reddit/symbolExtractor.py).

### symbolExtractor.py
The SymbolExtractors task is to scan a reddit submission for relevant stock tokens.

At construction the SymbolExtrator uses the [pyahocorasick](https://pypi.org/project/pyahocorasick/) library to build a finite state machine from a given CSV of stock token symbols.  
The AhoCorasick Algorithm, utilized by antiviral software, provides an efficient way to search for a multitude of search strings in one text.

The constructed automaton is then used to search in the title as well as in the post body for any stock symbols.

## Issues
Whilst implementing this data extraction algorithm, we ran into a multitude of problems, most of which we solved:

### Reddit API limitations
The Reddit API limits looking back in time to the 1000 most recent posts, but since we needed decidedly more data points than that,
we had to figure out a way around this limitation.

The solution we came up with, was to simply build a [daemon](../../RunRedditExtraction.py) that would request the new posts every 60 seconds.  
This daemon then ran on a debian server we rented for around 2 months.

### Incompatible Reddit post types
Since Reddit offers a bunch of multimedia options for posts, we blocked those out by simply ignoring every non-selfpost.  
This comes at the price of having less data to work with, and we would like to remedy this in the future,  
by either limiting the search to the title of multimedia posts or employing OCR or related technology to extract text.


### Stock token extraction
While looking for a way to extract stock tokens, the intuitive approach was to use a regex that would simply scan for two to four lettered combinations surrounded by spaces.
This lead to a bunch of problems, where posts would end or start with a stock tokens, People wouldn't properly use spaces etc.
Since the RegEx we used soon became too complicated to understand, we decided to change our approach to the string search described above.


### Finding a proper stock token list
Most libraries we tried to use either plain didn't work [e.g.](https://pypi.org/project/get-all-tickers/), or were not free of charge.

In the end we found a list of stock tokens that could be used in our library in a github release of one of the defunct libraries.
