# Extraction of Finance Data

The source files relevant to this discussion can be found [here](../../retrieval/Financial.py).

## Scope

This task mostly consists of fetching stock data for a given time frame and stock token.  
To do this, the [YahooFinance](https://algotrading101.com/learn/yahoo-finance-api-guide/) library is used.

## Implementation

As mentioned above, we utilize Yahoo Finance an open API which provides data on most stocks in the world.  
The library wraps the REST-API and collects current data as well as historical data required for older posts on reddit.

Our implementation provides some plots to plot out the stock data, and 2 functions to aggregate the data:

* is_stock_elevating: checks whether a stock is elevating over a given time frame
* average_slopes_of_stock: returns an array of average slopes of the stock in a specific time frame

Both these functions use the [best fitting line function of numpy](https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html) to fit a line into the data points of a time frame.

## Issues

There ware only two small issues with the collecting of the financial data.

1. Some stocks mentioned in Reddit posts did not exist in the Yahoo Finance Api, so we weren't able to collect their data and had to sort them out.
1. Some posts were that currently posted that there was no data yet, so we had to sort these posts out.