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
        from_emolex = [self.emolex[word] for word in sentence]

        if n > 2:
            frst_part = choose_emotions(from_emolex[:3], 0)
            last_part = choose_emotions(from_emolex[n-3:], 2)

            seq = map((lambda i: choose_emotions(from_emolex[i-1:i+2], 1)),
                      range(1, n-1))

            central_part = reduce(np.add, seq)

            result = frst_part + last_part + central_part
        elif n == 0:
            result = np.zeros(self.emotions_array_length,
                              dtype=np.int16)
        elif n == 1:
            result = choose_emotions(from_emolex, 0)
        elif n == 2:
            result = choose_emotions(from_emolex, 0) +\
                     choose_emotions(from_emolex, 1)

        return result
