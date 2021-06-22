import re
from get_all_tickers import get_tickers

# Fixme: This library is fucked, wait for fix or find a ticker list somewhere else
# tickers = get_tickers.get_tickers()


def extract_symbols_from_title(submission) -> list[str]:
    title = submission.title
    return extract_symbols_from_text(title)


def extract_symbols_from_self_text(submission) -> list[str]:
    if hasattr(submission, "self_text"):
        text = submission.self_text
        return extract_symbols_from_text(text)
    return []


def extract_symbols_from_text(text: str) -> list[str]:
    # matches stock symbols with a dollar at the start
    prefixed_matcher = r"(?:\s|\A)+[$]{1}([A-Z]{2,})(?=\s|\Z)+"
    # matches strings with 2 or more uppercase letters surrounded by whitespaces
    unprefixed_matcher = r"(?:\s|\A)+([A-Z]{2,})(?=\s|\Z)+"

    matches = re.findall(unprefixed_matcher, text)
    matches += re.findall(prefixed_matcher, text)
    return matches


def extract_symbols_from_submission(submission) -> list[str]:
    symbols: list[str] = extract_symbols_from_title(submission)
    symbols += extract_symbols_from_self_text(submission)
    return symbols
