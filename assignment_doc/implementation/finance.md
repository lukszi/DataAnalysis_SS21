# Extraction of Finance Data

The source files relevant to this discussion can be found [here](../../retrieval/Financial.py).

## Scope

The Financial part has manly one task.
To take a stock token and a time frame and collect the stock data of that
time period. For that task we use [YahooFinance](https://algotrading101.com/learn/yahoo-finance-api-guide/). It's an open source api with
which you are able to get many data of most of the stocks in the world.
It makes Http request to collected current data but also provides old data
which we need for older posts on the reddit.

The Financial source code also provides some plots to plot out the stock data
if desired. And 2 important functions to aggregate the data.

## Implementation

* is_stock_elevating: return whether a stock is elevating or not in a specific time frame
* average_slopes_of_stock: returns an array of average slopes of the stock in a specific time frame

Both these functions use the [best fitting line function of numpy](https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html) to fit a line into the data points of a time frame.

## Issues

There ware only two small issues with the collecting of the financial data.

1. Some stocks mentioned in Reddit posts did not exist in the Yahoo Finance Api, so we weren't able to collect their data and had to sort them out.
   

2. Some posts were that currently posted that there was no data yet, so we had to sort these posts out.