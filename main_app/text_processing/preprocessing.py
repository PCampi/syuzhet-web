"""Generic text preprocessing."""

import re


def preprocess_for_analysis(text):
    """Preprocess a text for tokenization.

    This will substitute all dialogues with fullstop-delimited sentences,
    all \"weak\" punctuation with a fullstop.

    Parameters
    ----------
    text : string
        the text to preprocess

    Returns
    -------
    processed_text : string
        the preprocessed text

    Examples
    --------
    >>> text = "Hello, I am Pietro. The cat is on the table: I don't like it."
    >>> preprocess(text)
    "Hello, I am Pietro. The cat is on the table. I don't like it."
    """
    return rebalance_full_stops(
        ellipsis(
            multiple_spaces(
                quotations_in_sentence(
                    guillements_in_sentence(
                        whitespace(
                            end_of_sentence(
                                apostrophe(text))))))))


def punctuation_to_space(text):
    """Substitute ?,!,;,:...- with a single space."""
    return re.sub(r'[?!;:\|\u2026\u2212\u002d\ufe63\uff0d\u2014\(\)]+',
                  r' ',
                  text)


def ellipsis(text):
    """Substitute ..+ with ."""
    return re.sub(r'[.]{2,}', r'.', text)


def rebalance_full_stops(text):
    """Substitute non consecutive full stops with one only."""
    return re.sub(r'\.(\s*\.*)*', r'. ', text)


def multiple_spaces(text):
    """Substitute multiple spaces with a single one, don't touch specials."""
    return re.sub(r'\s{2,}', r' ', text)


def whitespace(text):
    """Substitute all newlines and tabs with a single fullstop."""
    return re.sub(r'[\t\n\r\v\f]+', r'. ', text)


def apostrophe(text):
    """Substitute apostrophe with space."""
    return re.sub(r'[\u0027\u2019\u02bc]+', r' ', text)


def guillements_in_sentence(text):
    """Substitute all guillements in a sentence with a space."""
    return re.sub(r'[\u00ab]([^\u00bb]+)[\u00bb]', r' \1 ', text)


def quotations_in_sentence(text):
    """Substitute all opening-closing quotation marks with a space."""
    return re.sub(r'[\u0022]([^\u0022]+)[\u0022]', r' \1 ', text)


def end_of_sentence(text):
    """Put a space after each fullstop."""
    return re.sub(r'\.', r'. ', text)
