from typing import List

import pandas as pd
from ahocorapy.keywordtree import KeywordTree
from pandas import DataFrame, Series
from praw.models import Submission


class SymbolExtractor:
    """
    Takes a Reddit submission and extracts all mentioned tickers
    Utilizes the aho corasick algorithm known from antivirus software
    """

    __tickers: DataFrame
    __searchTree: KeywordTree

    def __init__(self, ticker_file: str):
        """
        Create new symbol extractor

        :param ticker_file: Path to a csv file with a Ticker column containing all relevant tickers
        """
        self.__tickers = pd.read_csv(ticker_file, sep="\t")
        self.__create_search_tree()

    def extract_symbols(self, submission: Submission) -> List[str]:
        """
        Extracts stock symbols from all text contained in a submission

        :param submission: to be searched
        :return: list of all found tickers
        """
        symbols: List[str] = self.__extract_symbols_from_title(submission)
        symbols += self.__extract_symbols_from_self_text(submission)
        symbols = self.__remove_duplicates(symbols)
        return symbols

    def __extract_symbols_from_title(self, submission: Submission) -> List[str]:
        """
        Extracts symbols from the title of a submission

        :param submission: to be searched
        :return: list of all found tickers
        """
        title = submission.title
        return self.find_symbols_in_text(title)

    def __extract_symbols_from_self_text(self, submission: Submission) -> List[str]:
        """
        Extracts symbols from the text of a submission

        :param submission: to be searched
        :return: list of all found tickers
        """
        if hasattr(submission, "self_text"):
            text = submission.self_text
            return self.find_symbols_in_text(text)
        return []

    def find_symbols_in_text(self, text: str) -> List[str]:
        """
        Extracts symbols from a text

        :param text: to be searched
        :return: List of all found tickers
        """
        matches = self.__searchTree.search_all(text)
        match_list = [ticker for (ticker, position) in matches]
        return match_list

    def __create_search_tree(self):
        """
        Initializes the search tree with the list of tickers in __tickers
        """
        self.__searchTree = KeywordTree()
        tickers: Series = self.__tickers.Ticker
        for ticker in tickers:
            self.__searchTree.add(ticker)
        self.__searchTree.finalize()

    @staticmethod
    def __remove_duplicates(symbols: List[str]):
        return list(set(symbols))


def main():
    extractor = SymbolExtractor("../../res/ticker.csv")
    print(extractor.__getattribute__("_SymbolExtractor__tickers"))


if __name__ == '__main__':
    main()
