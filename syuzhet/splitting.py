"""Sentence processing module"""

import nltk.tokenize
import nltk.data


class TextSplitter():
    """Split text into sentences or words."""

    def text_to_sentences(self, text, language):
        """Split a text into sentences.

        Parameters
        ----------
        text:
            the text to tokenize into sentences

        language:
            the language of the text

        Returns
        -------
        list:
            a list of strings, each of which is a sentence in the original text
        """
        # load the nltk data Punkt tokenizer for the selected language
        dict_path = "tokenizers/punkt/PY3/" + language.lower() + ".pickle"
        sentence_tokenizer = nltk.data.load(dict_path)
        # return the tokenized text
        return sentence_tokenizer.tokenize(text)

    def sentence_to_words(self, sentence, language):
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
        tokens = nltk.tokenize.word_tokenize(sentence, language=language)
        return [token.lower() for token in tokens]
