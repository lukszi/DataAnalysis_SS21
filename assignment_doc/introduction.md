# Data Analysis Project

This project aims to check whether posts made by reddits self-proclaimed "retards" on r/wallstreetbets, can in fact be used to predict market movements. 

## Introduction

### WallstreetBets
Since the start of the stock market craze in late 2020, one stock forum has repeatedly caught media attention.  
Be it due to the crass language, the extremely risky trades, or the introduction of so-called meme stocks through gamestop,
reddits WallStreetBets (WSB) forum has polarized financial media and consumer outlets alike.

This project asks whether the hype surrounding WSB is valid, and can be seen as a first step towards figuring out algorithms to capitalize on WSB posts by trying to predict market movements.

### Technical overview
To accomplish this, WSB posts have been extracted for the past two months, searched for stock symbols and then persisted into a local database.  
A correlation analysis between the collected data points, and the movement in stock prices over different durations has then been conducted.

## Implementation details
Details on how this marvelous feat of software engineering was accomplished, can be found here:
* [Reddit extraction](implementation/reddit_extraction.md)
* [Yahoo finance extraction](implementation/finance.md)
* [Data persistence](implementation/database.md)
* [Data evaluation](implementation/evaluation.md)

## Results
The results of our analysis can be found [here](results.md)

## Outlook
Since this project was only supposed to take two workdays, we focused on a minimum viable prototype, that could extract and analyse data in a basic manner.

However, we believe, that with more metrics, like for example a sentiment analysis of the reddit posts, and a more detailed analysis of the given data we could achieve a more accurate and potentially interesting result.