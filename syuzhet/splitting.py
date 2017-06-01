"""Sentence processing module"""
from typing import List
import nltk.tokenize
import nltk.data


class TextSplitter():
    """Split text into sentences or words."""

    def __init__(self, language):
        self.language = language

    def text_to_sentences(self, text: str,) -> List[str]:
        """Split a text into sentences.

        Parameters
        ----------
        text:
            the text to tokenize into sentences

        Returns
        -------
        list:
            a list of strings, each of which is a sentence in the original text
        """
        # load the nltk data Punkt tokenizer for the selected language
        dict_path = "tokenizers/punkt/PY3/" + self.language.lower() + ".pickle"
        sentence_tokenizer = nltk.data.load(dict_path)
        # return the tokenized text
        sentences = sentence_tokenizer.tokenize(text)
        return sentences

    def sentence_to_words(self, sentence: str) -> List[
            str]:
        """Get all the words in the sentence.

        Parameters
        ----------
        sentence:
            a string representing a single sentence

        Returns
        -------
        list:
            a list of lowercased words and punctuation tokens
        """
        tokens = nltk.tokenize.word_tokenize(sentence, language=self.language)
        result = [token.lower() for token in tokens]
        return result
