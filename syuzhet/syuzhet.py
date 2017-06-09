"""Main Syuzhet module."""
from typing import List
from functools import reduce
from itertools import tee
import numpy as np
import pudb

from .splitting import TextSplitter
from .lemmatization import Lemmatizer
from .emotion_filter import find_multiple_max


class SyuzhetNoFilter():
    """Syuzhet text analyzer class."""

    def emotions_for_sentence(self, sentence):
        """Get the emotions for a sentence.

        Parameters
        ----------
        sentence: List[str]
            the sentence to analyze; all words MUST be in EmoLex

        Returns
        -------
        np.ndarray
            an array of emotions for the sentence.
        """
        from_emolex = (self.emolex[word] for word in sentence)
        total = (reduce(np.logical_or, choices) for choices in from_emolex)
