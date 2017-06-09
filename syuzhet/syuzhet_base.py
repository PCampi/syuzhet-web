# coding: utf-8

"""Main Syuzhet module."""
from abc import ABC, abstractmethod
from typing import List
from functools import reduce
from itertools import tee
import numpy as np
import pudb

from .splitting import TextSplitter
from .lemmatization import Lemmatizer


class SyuzhetABC(ABC):
    """Base class for the Syuzhet text analyzer."""

    def __init__(self, language, tagger, emotions_array_length, emolex):
        """Initialize the class."""
        self.language = language
        self.tagger = tagger
        self.emotions_array_length = emotions_array_length
        self.emolex = emolex
        self.splitter = TextSplitter(self.language)

    def analyze_text(self, text, use_filter=True):
        """Extract emotions from a text.

        Parameters
        ----------
        text:
            the text to extract emotions from

        Returns
        -------
        numpy.array:
            the sum of all emotions found in the text
        """
        orig_sentences, to_lemmatize = tee(
            self.splitter.sentence_to_words(s)
            for s in
            self.splitter.text_to_sentences(text))

        # get the lemmatized sentences
        lemmatizer = Lemmatizer(self.tagger)
        lemmatized_sentences = (lemmatizer.lemmatize(s)
                                for s in to_lemmatize)

        # select the words: if the non lemmatized word is in EmoLex,
        # leave it there, otherwise choose the lemmatized one
        sents = [list(map((lambda x, y: x if x in self.emolex else y),
                          s, lemmatized_s))
                 for s, lemmatized_s
                 in zip(orig_sentences, lemmatized_sentences)]

        # filter the lemmatized sentences: only words in EmoLex
        # with emotion count > 0
        filtered_sentences = self.filter_sentences(sents)

        sentence_emotions = [self.emotions_for_sentence(s, use_filter)
                             for s in filtered_sentences]

        aggregate_result = reduce((lambda x, y: x + y),
                                  sentence_emotions).tolist()

        return {'aggregate': aggregate_result,
                'sentences': [arr.tolist() for arr in sentence_emotions]}

    def filter_sentences(self, sentences: List[List[str]]) -> List[List[str]]:
        """Filter the sentences, leaving only the words with emotion > 0."""
        def filter_func(word):
            """Convenience filtering function."""
            try:
                emotions = self.emolex[word]
                if len(emotions) == 1:
                    return np.sum(emotions[0]) > 0
                else:
                    has_value = False
                    i = 0
                    while (i < len(emotions)) and (not has_value):
                        has_value = np.sum(emotions[i]) > 0
                        i = i + 1

                    return has_value
            except KeyError as e:
                return False

        result = [[w for w in filter(filter_func, s)] for s in sentences]
        return result

    @abstractmethod
    def emotions_for_sentence(self, sentence):
        pass

        # for word in sentence:
        #     try:
        #         emotions = self.emolex[word]
        #         # FIXME: disambigua valenza
        #         result = result + emotions[0]
        #     except KeyError as e:
        #         pass

        # return result

    def _filter_func(self, word):
        """Function to filter out words with no emotional value."""
        try:
            emotions = self.emolex[word]
            if len(emotions) == 1:
                return np.sum(emotions[0]) > 0
            else:
                has_value = False
                i = 0
                while (i < len(emotions)) and (not has_value):
                    has_value = np.sum(emotions[i]) > 0
                    i = i + 1

                return has_value
        except KeyError as e:
            return False
