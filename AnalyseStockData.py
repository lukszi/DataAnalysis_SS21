import numpy as np
import pandas as pd

from database.DatabaseController import DatabaseController
from database.Model.StockMention import NUMBER_OF_STOCK_INFORMATION
from retrieval import Financial
import matplotlib.pyplot as plt


def analyse_stockdata_on_correlations_and_plot_some_interrelationships(number_of_days_after_post: int = 10):
    """
    Collects the stockdata to all reddit posts and analyse them on correlations
    :param number_of_days_after_post: How many days should be analysed after the reddit post has been done. (if to long data will probably not be found)
    """
    database_controller = DatabaseController("res/RedditStocks.db")
    stocks_mention = database_controller.get_stocks_mention_from_database()

    # collect all stockdata related to the reddit posts
    len_of_data = len(stocks_mention)
    stockdata = np.array([])
    i = 0
    print_progress_bar(0, len_of_data, prefix='Progress:', suffix='Complete', length=50)
    number_of_features = -1
    for (stock_mention, stock_token) in stocks_mention:
        slopes = Financial.average_slopes_of_stock(stock_token, stock_mention.posted,
                                                   max_days=number_of_days_after_post)
        if number_of_features == -1:
            number_of_features = NUMBER_OF_STOCK_INFORMATION + len(slopes)
        if slopes is not None and len(slopes) > 0:
            stockdata = np.append(stockdata, stock_mention.get_array_of_all_analysable_data())
            stockdata = np.append(stockdata, slopes)
        print_progress_bar(i + 1, len_of_data, prefix='Progress:', suffix='Complete', length=50)
        i += 1

    # convert stockdata to analyse
    stockdata = np.reshape(stockdata, (int(len(stockdata) / number_of_features), number_of_features))
    stockdata = stockdata.astype('float64')

    # analyse converted stockdata
    calculate_covarianz_for_lineare_correlations(stockdata)
    plot_upvote_ratio_against_average_slope(stockdata)
    plot_num_of_likes_against_average_slope(stockdata)
    plot_num_of_comments_against_average_slope(stockdata)


def calculate_covarianz_for_lineare_correlations(stockdata):
    """
    Calculates the Correlation matrix to the stockdata and saves it in a csv file
    :param stockdata: on which to calculate the Correlations
    """
    values = np.delete(stockdata, 0, axis=1)
    cov = np.corrcoef(values.T.astype(float))
    pd.DataFrame(cov).to_csv("res/Grafics/Covarianz.csv", sep=";")


def plot_upvote_ratio_against_average_slope(stockdata):
    """
    Plots the Up-Vote Ratio against the average slope of all stocks
    :param stockdata: on which to plot the results
    """
    x = stockdata[:, 3]
    for y_index in range(4, stockdata.shape[1]):
        y = stockdata[:, y_index]
        plt.scatter(x, y)
        plt.xlabel("Up-Vote Ratio")
        plt.ylabel(f"Average slope after {y_index - 5} days")
        plt.figtext(.1, .9, f"Mean of Up-Vote Ratio : {x.mean()}\n")
        plt.figtext(.1, .9, f"Mean of Average Slope after {y_index - 5} days : {y.mean()}")
        plt.axis((0, 1, -1, 1))
        plt.savefig(f'res/Grafics/UpVoteRatioWithAverageSlopeAfter{y_index - 5}Days.png')
        plt.show()


def plot_num_of_likes_against_average_slope(stockdata):
    """
    Plots the Number of Up-votes against the average slope of all stocks
    :param stockdata: on which to plot the results
    """
    x = stockdata[:, 1]
    for y_index in range(4, stockdata.shape[1]):
        y = stockdata[:, y_index]
        plt.scatter(x, y)
        plt.xlabel("Number of Up-votes")
        plt.ylabel(f"Average slope after {y_index - 5} days")
        plt.figtext(.1, .9, f"Mean of Number of Up-votes : {x.mean()}\n")
        plt.figtext(.1, .9, f"Mean of Average Slope after {y_index - 5} days : {y.mean()}")
        plt.axis((0, None, -1, 1))
        plt.savefig(f'res/Grafics/UpVotesWithAverageSlopeAfter{y_index - 5}Days.png')
        plt.show()


def plot_num_of_comments_against_average_slope(stockdata):
    """
    Plots the Number of Comments against the average slope of all stocks
    :param stockdata: on which to plot the results
    """
    x = stockdata[:, 4]
    for y_index in range(4, stockdata.shape[1]):
        y = stockdata[:, y_index]
        plt.scatter(x, y)
        plt.xlabel("Number of comments")
        plt.ylabel(f"Average slope after {y_index - 5} days")
        plt.figtext(.1, .9, f"Mean of Number of Comments : {x.mean()}\n")
        plt.figtext(.1, .9, f"Mean of Average Slope after {y_index - 5} days : {y.mean()}")
        plt.axis((0, None, -1, 1))
        plt.savefig(f'res/Grafics/UpVotesWithAverageSlopeAfter{y_index - 5}Days.png')
        plt.show()


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    analyse_stockdata_on_correlations_and_plot_some_interrelationships(21)
