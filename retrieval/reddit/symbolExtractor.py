import pandas as pd
from ahocorapy.keywordtree import KeywordTree
from pandas import DataFrame, Series


class SymbolExtractor:

    __tickers: DataFrame
    __searchTree: KeywordTree

    def __init__(self, ticker_file: str):
        self.__tickers = pd.read_csv(ticker_file, sep="\t")
        self.__create_search_tree()

    def extract_symbols(self, submission) -> list[str]:
        symbols: list[str] = self.__extract_symbols_from_title(submission)
        symbols += self.__extract_symbols_from_self_text(submission)
        return symbols

    def __extract_symbols_from_title(self, submission) -> list[str]:
        title = submission.title
        return self.find_symbols_in_text(title)

    def __extract_symbols_from_self_text(self, submission) -> list[str]:
        if hasattr(submission, "self_text"):
            text = submission.self_text
            return self.find_symbols_in_text(text)
        return []

    def find_symbols_in_text(self, text: str) -> list[str]:
        matches = self.__searchTree.search_all(text)
        match_list = [ticker for (ticker, position) in matches]
        return match_list

    def __create_search_tree(self):
        self.__searchTree = KeywordTree()
        tickers: Series = self.__tickers.Ticker
        for ticker in tickers:
            self.__searchTree.add(ticker)
        self.__searchTree.finalize()


def main():
    extractor = SymbolExtractor("ticker.csv")
    print(extractor.__tickers)


if __name__ == '__main__':
    main()
