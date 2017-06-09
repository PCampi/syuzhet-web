from functools import reduce
import numpy as np

from .syuzhet_base import SyuzhetABC
from .emotion_filter import choose_emotions


class SyuzhetWithFilter(SyuzhetABC):
    """Syuzhet text analyzer class, no filter version."""

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
        n = len(sentence)

        if n == 0:
            return np.zeros(self.emotions_array_length,
                            dtype=np.int16)

        from_emolex = [self.emolex[word] for word in sentence]

        if n == 1:
            result = choose_emotions(from_emolex, 0, 0)
            return result
        if n == 2:
            result = choose_emotions(from_emolex, 0, 0) +\
                     choose_emotions(from_emolex, 0, 1)

        if n > 2:
            frst_part = choose_emotions(from_emolex[:3], 0, 0)
            last_part = choose_emotions(from_emolex[n-3:], 0, 2)

            seq = map((lambda i: choose_emotions(from_emolex[i-1:i+2], 0, 1)),
                      range(1, n-1))

            central_part = reduce(np.add, seq)

            result = frst_part + last_part + central_part
            return result
