from datetime import datetime, timedelta

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


def is_stock_elevating(stock_token: str, start: str, time_delta_in_days: int) -> bool:
    """
    returns a boolean whether the stock is elevating in time_delta_in_days from the start
    :param stock_token:
    :param start: start date of evaluation
    :param time_delta_in_days: how many days from start of evaluation should be included
    :return: True if Stock of stock_token is elevating else false
    """
    ticker = yf.Ticker(stock_token)
    # calculate end
    date_parts = start.split('-')
    date_parts[2] = str(int(date_parts[2]) + time_delta_in_days).zfill(2)
    end = '-'.join(date_parts)

    dataframe = ticker.history(start=start, end=end, interval='1h')
    m, b = calculate_best_fitting_line(dataframe)
    # plot_dataframe(dataframe)
    print(m, b)
    if m > 0:
        return True
    return False


def how_many_days_after_stock_elevates(stock_token: str, start: str, max_days: int = 10) -> int:
    ticker = yf.Ticker(stock_token)

    start_datetime = datetime.fromisoformat(start)
    timedelta_max_days = timedelta(days=max_days)
    end_datetime = start_datetime + timedelta_max_days
    end = end_datetime.strftime('%Y-%m-%d')
    dataframe = ticker.history(start=start, end=end, interval='1h')
    print(dataframe)



def calculate_best_fitting_line(dataframe) -> (int, int):
    """
    Calculates the best fitting line of points in dataframe
    :param dataframe: dataframe with points
    :return: Gradient and y axis intercept
    """
    y = dataframe['Close']
    x = range(dataframe.shape[0])
    m, b = np.polyfit(x, y, 1)
    plot_line_with_data_points(x, y, m, b)
    return m, b


def plot_line_with_data_points(x, y, m, b) -> None:
    """
    Plots all datapoints x and y with a line crated from m and b
    :param x: x coordinates
    :param y: y coordinates
    :param m: Gradient of line
    :param b: y axis intercept of Line
    :return:None
    """
    plt.plot(x, y, 'o')
    plt.plot(x, m * x + b)
    plt.show()


def plot_dataframe(dataframe) -> None:
    """
    Plots the ['Close'] coordinates of the dataframe
    :param dataframe:
    :return: None
    """
    dataframe['Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted")
    plt.show()


def plot_stock(stock_token: str, start: str, end: str) -> None:
    """
    Plots a stock from a start date to the end date
    :param stock_token: token of stock which should be ploted
    :param start: start date in format "YYYY-MM-DD"
    :param end: end date in format "YYYY-MM-DD"
    :return: None
    """
    ticker = yf.Ticker(stock_token)
    dataframe = ticker.history(start=start, end=end)
    plot_dataframe(dataframe)


if __name__ == '__main__':
    # print(is_stock_elevating('TSLA', "2021-02-01", 25))
    # print(is_stock_elevating('CLOV', "2021-02-01", 25))
    # print(is_stock_elevating('WSB', "2021-03-22", 5))

    how_many_days_after_stock_elevates('TSLA', "2021-02-01", 20)

