# WallStreetBets DataAnalysis project

This repository is the DataAnalysis project by Lukas (3217694), Benno (3254806) and Marco (3195666)

The goal of this project is to extract mentions of stocksymbols from reddits wallstreetbets, and then search for 
correlations in mention spikes and stock price shifts.

## Documentation
The required documentation can be found in the [asignment_doc](assignment_doc/introduction.md) folder

## Setup
### Python
* Setup a Python 3.9 virtualenv
    * ```py -m venv env```
* Activate virtualenv
    * ```.\env\Scripts\activate```
* Install dependencies
    * ```pip install -r requirements.txt```
### Reddit
* rename or copy ``./res/reddit_config.json.example`` to ``./res/reddit_config.json``
* Open ``./res/reddit_config.json`` and fill all fields with [your reddit API credentials](https://old.reddit.com/prefs/apps)

## Run
### Data Extraction
```py RunRedditExtraction.py```
