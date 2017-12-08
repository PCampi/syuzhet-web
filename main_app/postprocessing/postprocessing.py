"""Postprocessing module for Syuzhet."""

import numpy as np
from .fourier import low_pass_filter


def smooth_emotions(emotions, number_of_harmonics=5,
                    method='fft', frequencies=False):
    """Smooth emotions.

    Parameters
    ----------
    emotions: np.ndarray
        array of emotion values. Can be a 1D array or 2D array, in which case
        every column is considered an emotion and every row a time point

    number_of_harmonics: int
        how many frequencies to retain in the low-pass filter

    method: str
        either "fft" for Complex Fourier Transform or "rfft" for Real
        Fourier Transform

    frequencies: bool
        if True, also return the frequency spectrum of the signal

    Returns
    -------
    smoothed: np.ndarray
        array which is the application of the low-pass filter to "emotions".

    (only if frequencies=True)
    freqs: np.ndarray
        array of frequencies in the signal
    """
    if len(emotions.shape) == 1:  # it's an array
        smoothed, freqs = low_pass_filter(emotions, number_of_harmonics,
                                          method)
    elif len(emotions.shape) == 2:  # it's a matrix
        smoothed = np.zeros(emotions.shape)
        freqs = np.zeros(emotions.shape)

        for j in range(emotions.shape[1]):
            smoothed[:, j], freqs[:, j] = low_pass_filter(
                                            emotions[:, j],
                                            number_of_harmonics,
                                            method)
    else:
        raise ValueError("Emotions must be a 1D or 2D numpy array. " +
                         "It is a {} array".format(len(emotions.shape)))

    if frequencies:
        return smoothed, freqs
    else:
        return smoothed


def normalize(v):
    """Normalize a numpy array or matrix based on the maximum value.

    Parameters
    ----------
    v:
        a np.array which is either a single row or a matrix; shape longers than
        2 are not supported

    Returns
    -------
    np.array:
        an array with the same shape as the original, normalized on the maximum
        value occurring in the original; works on columns if matrix input
    """
    # if it's an array, normalize on the maximum value
    if len(v.shape) == 1:
        return v / np.max(v)
    # if it's a 2D matrix, normalize by column
    elif len(v.shape) == 2:
        normalized = np.zeros(v.shape)

        for i in range(v.shape[1]):
            normalized[:, i] = normalize(v[:, i])

        return normalized


def clean_less_than_zero(ref_values, v):
    """Strip all non zeros values from v, if ref_values are zero."""
    return np.where(ref_values > 0, v, 0)
