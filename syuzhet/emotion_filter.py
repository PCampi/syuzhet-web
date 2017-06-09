"""Module for filtering emotions of a word based on the context."""
from functools import reduce
import numpy as np
# import pudb


def choose_emotions(arr, start, reference_index, keep_more=False):
    """Choose the winning emotions in a sentence window.

    Parameters
    ----------
    arr: List[List[np.ndarray]]
        a list of arrays representing the subsentence under consideration

    start: int
        index at which the real emotions start

    reference_index: int
        the index of the word under consideration

    Returns
    -------
    result: List[int]
        list of positions where the winning emotion(s) are located
        in the emotion array of the reference word
    """
    summed = [reduce(np.add, l) for l in arr]
    curr = summed[reference_index]
    emo_shape = np.shape(curr)
    context = [summed[i] for i in range(len(summed)) if i != reference_index]

    if len(context) > 0:
        context_or = reduce(np.logical_or, context)
        result = __get_max_overlap(curr, context_or)
    else:
        max_indexes = find_multiple_max(curr)
        result = __array_with_indexes_and_shape(max_indexes, emo_shape)

    return result


def __get_max_overlap(current_sum, context_or):
    """Check that the current array and the context have overlap.

    Parameters
    ----------
    current_sum: np.ndarray
        array of emotions for the current word (already reduced with +)

    context_or: np.ndarray
        boolean array of emotions for the context (already reduced with or)

    Returns
    -------
    np.ndarray, dtype=np.int16 as bool
        emotions array for current word, if its maximum value is also in the
        context, otherwise the emotion(s) with highest intensity in current_sum
    """
    result = None
    curr_sum = current_sum.copy()
    emo_shape = np.shape(curr_sum)
    max_indexes = set()
    general_max_indexes = set()

    while result is None and np.sum(curr_sum) > 0:
        curr_and_context = np.logical_and(context_or,
                                          curr_sum).astype(np.int16)

        if np.sum(curr_and_context) > 0:
            # check that the max value of current is in common with context
            max_indexes = find_multiple_max(curr_sum)
            general_max_indexes = general_max_indexes.union(set(max_indexes))
            max_to_keep = list(filter((lambda i: context_or[i] > 0),
                                      max_indexes))

            if len(max_to_keep) > 0:  # the max is in common with context
                result = __array_with_indexes_and_shape(max_to_keep,
                                                        emo_shape)
            else:  # the max is not in common -> retry without the current max
                curr_sum = np.zeros(np.shape(curr_sum), dtype=np.int16)
                for i in range(np.shape(curr_sum)[0]):
                    if i not in general_max_indexes:
                        curr_sum[i] = current_sum[i]
        else:  # there is no overlap -> return the max value in current_sum
            max_indexes = find_multiple_max(current_sum)
            result = np.zeros(np.shape(current_sum), dtype=np.int16)
            for i in max_indexes:
                result[i] = 1

    if result is None:
        max_indexes = find_multiple_max(current_sum)
        result = np.zeros(np.shape(current_sum), dtype=np.int16)
        for i in max_indexes:
            result[i] = 1

    return result


def find_multiple_max(arr, return_value=False):
    """Find all occurrences of the maximum value inside an array.

    Parameters
    ----------
    arr: np.ndarray
        array of which to find the max value indexes

    Returns
    -------
    max_value, max_indexes: Tuple[int, List[int]]
        max_value is the numeric value of the max,
        max_indexes is a List of all the positions where it occurs
    """
    max_value = arr[0]
    max_indexes = [0]
    for i in range(1, len(arr)):
        current_value = arr[i]
        if current_value == max_value:
            max_indexes.append(i)
        elif current_value > max_value:
            max_value = current_value
            max_indexes = [i]

    if return_value:
        return max_value, max_indexes
    else:
        return max_indexes


def __array_with_indexes_and_shape(indexes, shape):
    """Create a np.ndarray with 1 in the positions in indexes."""
    result = np.zeros(shape, dtype=np.int16)
    for index in indexes:
        result[index] = 1

    return result
