from datetime import datetime, timedelta

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

NUMBER_OF_ENTRIES_A_DAY = 7


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
    m, b = calculate_best_fitting_line(range(dataframe.shape[0]), dataframe['Close'].values)
    print(f'm={m} , b={b}')
    if m > 0:
        return True
    return False


def average_slopes_of_stock(stock_token: str, start_datetime: datetime, max_days: int = 10, plot_data: bool = False) -> \
        np.ndarray or None:
    """
    List of average slopes of the stock from the start in 1 to max_days-1 days intervals
    :param start_datetime: start datetime
    :param plot_data: True if the data and best fitting line should be ploted
    :param stock_token: the specific stock token
    :param max_days: how many days after start you want to have the average slopes
    :return: List of average slopes
    """
    ticker = yf.Ticker(stock_token)
    # calculate start and end date
    timedelta_max_days = timedelta(days=max_days)
    end_datetime = start_datetime + timedelta_max_days
    start = start_datetime.strftime('%Y-%m-%d')
    end = end_datetime.strftime('%Y-%m-%d')
    # get tickers history
    dataframe = ticker.history(start=start, end=end, interval='1h')
    close = dataframe['Close'].values
    if len(close) > 0:
        # calculate best fitting line from start in interval_day steps
        elevations = np.zeros(17)
        i = 0
        for interval_day in range(1, max_days - 1):
            number_of_entries = int(interval_day * NUMBER_OF_ENTRIES_A_DAY)
            interval_close = close[0:number_of_entries]
            if i <= 16:
                m, b = calculate_best_fitting_line(range(len(interval_close)), interval_close, plot_data)
                if np.isnan(m):
                    return None
                elevations[i] = m
            i += 1
        if elevations[0] != np.nan:
            return elevations
    return None


def calculate_best_fitting_line(x, y, plot_data: bool = False) -> (int, int):
    """
    Calculates the best fitting line of points in dataframe
    :param y: Y-Coordinates
    :param x: X-Coordinates
    :param plot_data: whether the data and line should be plotted (default = False)
    :return: Gradient and y axis intercept
    """
    # y = dataframe['Close']
    # x = range(dataframe.shape[0])
    try:
        m, b = np.polyfit(x, y, 1)
    except:
        return 0, 0
    if plot_data:
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
    print(is_stock_elevating('TSLA', "2021-02-01", 25))
    print(is_stock_elevating('CLOV', "2021-02-01", 25))
    start_datetime = datetime.fromisoformat("2021-02-01")
    stocks_slope = average_slopes_of_stock('TSLA', start_datetime, 8, plot_data=True)
    print(stocks_slope)
