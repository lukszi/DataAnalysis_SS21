import re
import pandas as pd
from ahocorapy.keywordtree import KeywordTree
from pandas import DataFrame
import numpy as np


class SymbolExtractor:

    tickers: DataFrame
    searchTree: KeywordTree

    def __init__(self, ticker_file: str):
        self.tickers = pd.read_csv(ticker_file, sep="\t")
        self.create_search_tree()

    def extract_symbols(self, submission) -> list[str]:
        symbols: list[str] = self.extract_symbols_from_title(submission)
        symbols += self.extract_symbols_from_self_text(submission)
        return symbols

    def extract_symbols_from_title(self, submission) -> list[str]:
        title = submission.title
        return self.find_symbols_in_text(title)

    def extract_symbols_from_self_text(self, submission) -> list[str]:
        if hasattr(submission, "self_text"):
            text = submission.self_text
            return self.find_symbols_in_text(text)
        return []

    def find_symbols_in_text(self, text: str) -> list[str]:
        matches = self.searchTree.search_all(text)
        match_list = [ticker for (ticker, position) in matches]
        return match_list

    def create_search_tree(self):
        self.searchTree = KeywordTree()
        tickers: np.array = self.tickers.Ticker
        for ticker in np.nditer(tickers):
            self.searchTree.add(ticker)
        self.searchTree.finalize()


def main():
    extractor = SymbolExtractor("test.csv")
    print(extractor.tickers)


if __name__ == '__main__':
    main()
