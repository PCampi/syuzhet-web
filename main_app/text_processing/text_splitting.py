"""Sentence processing module."""

from typing import List

import nltk.data
import nltk.tokenize


def text_to_sentences(text: str, language: str) -> List[str]:
    """Splits a text into sentences.

    Parameters
    ----------
    text:
        the text to tokenize into sentences

    Returns
    -------
    List[str]:
        a list of strings, each of which is a sentence in the original text
    """
    # load the nltk data Punkt tokenizer for the selected language
    dict_path = "tokenizers/punkt/PY3/" + language.lower() + ".pickle"
    sentence_tokenizer = nltk.data.load(dict_path)
    # return the tokenized text
    sentences = sentence_tokenizer.tokenize(text)
    return sentences


def sentence_to_words(sentence: str, language: str) -> List[str]:
    """Get all the words in the sentence.

    Parameters
    ----------
    sentence: str
        a string representing a single sentence

    Returns
    -------
    List[str]:
        a list of lower cased words and punctuation tokens
    """
    tokens = nltk.tokenize.word_tokenize(sentence, language=language)
    result = [token.lower() for token in tokens]
    return result
