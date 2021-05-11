import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


def is_stock_elevating(stock_token: str, start: str, time_delta_in_days: int) -> bool:
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


def calculate_best_fitting_line(dataframe):
    y = dataframe['Close']
    x = range(dataframe.shape[0])
    m, b = np.polyfit(x, y, 1)
    plot_line_with_data_points(x, y, m, b)
    return m, b


def plot_line_with_data_points(x, y, m, b):
    plt.plot(x, y, 'o')
    plt.plot(x, m * x + b)
    plt.show()


def plot_dataframe(dataframe):
    dataframe['Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted")
    plt.show()


def plot_stock(stock_token: str, start: str, end: str):
    ticker = yf.Ticker(stock_token)
    dataframe = ticker.history(start=start, end=end)
    plot_dataframe(dataframe)


if __name__ == '__main__':
    print(is_stock_elevating('TSLA', "2021-02-01", 25))
