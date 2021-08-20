# Data Analysis Project

The goal of this project is to extract mentions of stocksymbols from reddits wallstreetbets, and then search for 
correlations in mention spikes and stock price shifts.

## Introduction

The project should use an api to extract many stocks mentioned on a subreddit 
called WallStreetBets. It's a public forum where people post, argue and comment 
on stuff about the stock market.

With the extraction of the stock token and the time the post was made the 
program should be able to get the specific stock data. And saves it in a
database to be analysed later on.

The goal is to find out weather the post have an impact on the stock.
To find that out the program searches for correlations between the 
stock data, and the data from the reddit post. The idea is to find a 
correlation between something like the number of likes and the average slope
of the stock.
