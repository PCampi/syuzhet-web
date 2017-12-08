"""Syuzhet module with no filter."""

from functools import reduce
from typing import List

import numpy as np

from .syuzhet_base import SyuzhetABC


class SyuzhetNoFilter(SyuzhetABC):
    """Syuzhet text analyzer class, no filter version."""

    def emotions_for_sentence(self, sentence: List[str]):
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
        if sentence == []:
            return np.zeros((self.emotions_array_length,),
                            dtype=np.int16)

        from_emolex = (self.emolex[word] for word in sentence)
        all_words = (reduce(np.logical_or, choices).astype(np.int16)
                     for choices in from_emolex)
        result = reduce(np.add, all_words)

        return result
