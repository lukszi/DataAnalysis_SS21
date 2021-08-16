This repository is the DataAnalysis project by Lukas (3217694), Benno (3254806) and Marco (Add matrNr)

The goal of this project is to extract mentions of stocksymbols from reddits wallstreetbets, and then search for 
correlations in mention spikes and stock price shifts.

Currently implemented is the extraction of symbols utilizing PRAW, a stocksymbol list and the aho-corasick algorithm,
the extraction of financial data from yahoo finance and a database persisting the extracted data.

# Setup
## Python
* Setup a Python 3.9 virtualenv
    * ```py -m venv env```
* Activate virtualenv
    * ```.\env\Scripts\activate```
* Install dependencies
    * ```pip install -r requirements.txt```
## Reddit
* rename or copy ``./res/reddit_config.json.example`` to ``./res/reddit_config.json``
* Open ``./res/reddit_config.json`` and enter all fields with the right information from https://old.reddit.com/prefs/apps

# Run
## Data Extraction
```py RunRedditExtraction.py```