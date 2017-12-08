"""Main Syuzhet module."""

from abc import ABC, abstractmethod
from functools import reduce
from itertools import tee
from typing import List

import numpy as np

from ..text_processing import sentence_to_words, text_to_sentences
from .lemmatization import Lemmatizer
from .preprocessing import preprocess_for_analysis


class SyuzhetABC(ABC):
    """Base class for the Syuzhet text analyzer."""

    def __init__(self, language, tagger, emotions_array_length, emolex):
        """Initialize the class."""
        self.language = language
        self.tagger = tagger
        self.emotions_array_length = emotions_array_length
        self.emolex = emolex

    def analyze_text(self, text: str, get_sentences=False,
                     return_sentence_str=False, preprocess=False):
        """Extract emotions from a text.

        Parameters
        ----------
        text: str
            the text to extract emotions from

        get_sentences: bool
            if True, also return the tokenized sentences

        return_sentence_str: bool
            if True, also return the list of sentences as a list of str

        preprocess: bool
            if True, preprocess all dialogues and punctuation for better
            tokenization

        Returns
        -------
        dict:
            dictionary with keys
            - "aggregate": the aggregate emotional value of the text
            - "sentences": list of per-sentence emotion array
            - "sentence_list": list of lists of strings, each one a sentence
            - "sentences_as_str": list of strings, each one a sentence
        """
        if preprocess:
            preprocessed_text = preprocess_for_analysis(text)
            sentences_str = text_to_sentences(preprocessed_text,
                                              language=self.language)
        else:
            sentences_str = text_to_sentences(text,
                                              language=self.language)

        if get_sentences:
            orig_sentences, to_lemmatize, sent_to_return = tee(
                (sentence_to_words(s, self.language)
                 for s in sentences_str), 3)
        else:
            orig_sentences, to_lemmatize = tee(
                sentence_to_words(s, self.language)
                for s in sentences_str)

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

        sentence_emotions = [self.emotions_for_sentence(s)
                             for s in filtered_sentences]

        default_value = np.zeros(self.emotions_array_length, dtype=np.int16)

        aggregate_result = reduce(np.add, sentence_emotions, default_value)

        result = {'aggregate': aggregate_result,
                  'sentences': sentence_emotions}

        if get_sentences:
            result['sentence_list'] = list(map(list, sent_to_return))

        if return_sentence_str:
            result['sentences_as_str'] = sentences_str

        return result

    def filter_sentences(self, sentences: List[List[str]]) -> List[List[str]]:
        """Filter the sentences, leaving only the words with emotion > 0."""
        def filter_func(word):
            """Convenience filtering function."""
            try:
                emotions = self.emolex[word]
                if len(emotions) == 1:
                    return np.sum(emotions[0]) > 0

                has_value = False
                i = 0
                while (i < len(emotions)) and (not has_value):
                    has_value = np.sum(emotions[i]) > 0
                    i = i + 1

                return has_value
            except KeyError:
                return False

        result = [[w for w in filter(filter_func, s)] for s in sentences]
        return result

    @abstractmethod
    def emotions_for_sentence(self, sentence: List[str]):
        """Main method."""
        pass

    def _filter_func(self, word):
        """Function to filter out words with no emotional value."""
        try:
            emotions = self.emolex[word]
            if len(emotions) == 1:
                return np.sum(emotions[0]) > 0

            has_value = False
            i = 0
            while (i < len(emotions)) and (not has_value):
                has_value = np.sum(emotions[i]) > 0
                i = i + 1

            return has_value
        except KeyError:
            return False
