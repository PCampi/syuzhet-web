"""Functions that perform filtering on the original signal."""

import numpy as np
from scipy.fftpack import fft, ifft, rfft, irfft


def low_pass_filter(signal, low_pass_size=5, method='fft'):
    """Apply low pass filter to the signal.

    Parameters
    ----------
    signal:
        signal to apply the filter on

    low_pass_size:
        number of harmonics to keep when transforming

    method:
        either 'fft' (complex values) or 'rfft' (real values)

    Returns
    -------
    (np.array, np.array):
        tuple where the first element is the filtered time signal,
        the second is the frequency spectrum of the original signal
    """
    # compute FFT
    spectrum = _transform(signal, method)
    frequencies = np.copy(spectrum)

    # cut the higher frequencies and return the inverse
    spectrum[low_pass_size:-low_pass_size] = 0.0

    return _antitransform(spectrum, method), frequencies


def _transform(time_signal, method='fft'):
    """Transform a signal with Fourier."""
    if method == 'fft':
        return fft(time_signal)
    elif method == 'rfft':
        return rfft(time_signal)


def _antitransform(freq_signal, method='fft'):
    """Go back to the time domain, given the frequency transform."""
    if method == 'fft':
        return np.real(ifft(freq_signal))
    elif method == 'rfft':
        return irfft(freq_signal)
