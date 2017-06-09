"""Test for the emotion filtering algorithm."""
import unittest
import numpy as np
from functools import reduce
import pudb

from .emotion_filter import __find_multiple_max as multiple_max
from .emotion_filter import choose_emotions
from .emotion_filter import __get_max_overlap as max_overlap


class EmotionFilteringTest(unittest.TestCase):
    """Test for the module emotion_filter."""

    def testThatItChoosesEmotions(self):
        """Test for the function `choose_emotions`."""
        prev, curr, nxtw = self.createTestInput()
        p = [reduce(np.add, prev)]
        c = [reduce(np.add, curr)]
        n = [reduce(np.add, nxtw)]

        computed = choose_emotions([p, c, n],
                                   1,
                                   1,
                                   False)
        expected = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0], dtype=np.int16)

        self.assertNdarrayEqual(computed, expected, "Results differ")

    def testThatItChoosesEmotions2(self):
        """Test for the function `choose_emotions`."""
        prev, curr, nxtw = self.createTestInput2()
        p = [reduce(np.add, prev)]
        c = [reduce(np.add, curr)]
        n = [reduce(np.add, nxtw)]

        computed = choose_emotions([p, c, n],
                                   1,
                                   1,
                                   False)
        expected = np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 0], dtype=np.int16)

        self.assertNdarrayEqual(computed, expected, "Results differ")

    # next test to write:
    # testThatItChoosesEmotionsWithOnly2Words:
    # test that it works even if the context is a single array
    # testThatItChoosesEmotionsWithOnly1Word
    # test that it works even with a single word, must return the max
    # value of the word

    def testThatItFindsOverlap(self):
        """Test for the `__get_max_overlap` function."""
        current_sum = np.array([0, 0, 1, 2, 0, 3, 0, 0, 1, 0],
                               dtype=np.int16)
        context_or = np.array([False, True, False, True, False,
                               False, True, True, True, False])
        computed = max_overlap(current_sum, context_or)
        expected = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            dtype=np.int16)
        self.assertNdarrayEqual(computed, expected,
                                " Arrays differ")

        # pudb.set_trace()
        current_sum = np.array([0, 0, 4, 0, 0, 3, 0, 0, 1, 0],
                               dtype=np.int16)
        context_or = np.array([False, True, False, True, False,
                               False, True, True, True, False])
        computed = max_overlap(current_sum, context_or)
        expected = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                            dtype=np.int16)
        self.assertNdarrayEqual(computed, expected,
                                " Arrays differ")

    def testThatItFindsCorrectMax(self):
        """Test for the `__find_multiple_max` function."""
        arr = np.array([0, 1, 0, 4, 1, 3, 2, 0, 3, 4],
                       dtype=np.int16)
        max_val, max_indexes = multiple_max(arr, True)

        expected_max_val = 4
        expected_max_indexes = [3, 9]

        self.assertEqual(max_val, expected_max_val, "Max values are different")
        self.assertEqual(max_indexes, expected_max_indexes,
                         "Max indexes are different")

        max_ind = multiple_max(arr)
        self.assertEqual(max_ind, expected_max_indexes,
                         "Max indexes are different")

    def createTestInput(self):
        """Create input values for the test."""
        prev = [[0, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                [0, 1, 1, 0, 0, 1, 0, 1, 0, 1]]
        curr = [[1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 0]]
        nxtw = [[1, 0, 0, 0, 0, 0, 0, 1, 1, 0]]

        p = [self.createNpArray(a) for a in prev]
        c = [self.createNpArray(a) for a in curr]
        n = [self.createNpArray(a) for a in nxtw]

        return p, c, n

    def createTestInput2(self):
        """Create input values for the test."""
        prev = [[0, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                [0, 1, 1, 0, 0, 1, 0, 1, 0, 1]]
        curr = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]
        nxtw = [[1, 0, 0, 0, 0, 0, 0, 1, 1, 0]]

        p = [self.createNpArray(a) for a in prev]
        c = [self.createNpArray(a) for a in curr]
        n = [self.createNpArray(a) for a in nxtw]

        return p, c, n

    def createNpArray(self, lst):
        """Create np.ndarrays with np.int16 dtype."""
        return np.array(lst, dtype=np.int16)

    def assertNdarrayEqual(self, a1, a2, msg=""):
        """Same as assertEqual but for numpy arrays."""
        if not isinstance(a1, np.ndarray):
            raise TypeError("First argument is not a np.ndarray")

        if not isinstance(a2, np.ndarray):
            raise TypeError("Second argument is not a np.ndarray")

        self.assertEqual(np.shape(a1), np.shape(a2), msg +
                         " Lengths of lists are different.")

        if not np.array_equal(a1, a2):
            raise AssertionError(" Arrays are different according to numpy")
