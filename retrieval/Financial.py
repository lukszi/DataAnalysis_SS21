import yfinance as yf
import matplotlib.pyplot as plt

if __name__ == '__main__':
    ticker = yf.Ticker('TSLA')
    dataframe_of_year = ticker.history(start="2021-01-01", end="2021-02-01")

    dataframe_of_year['Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted")
    plt.show()
