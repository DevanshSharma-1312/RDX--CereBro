import numpy as np
from scipy.signal import butter, filtfilt, iirnotch


FS = 250


def remove_dc(signal):
    """Remove DC offset."""
    return signal - np.mean(signal)


def bandpass_filter(signal, lowcut=0.5, highcut=45, fs=FS, order=4):
    """Apply Butterworth bandpass filter."""

    nyquist = fs / 2

    low = lowcut / nyquist
    high = highcut / nyquist

    b, a = butter(
        order,
        [low, high],
        btype="band"
    )

    return filtfilt(b, a, signal)


def notch_filter(signal, freq=50, fs=FS, quality=30):
    """Remove power-line interference."""

    b, a = iirnotch(
        freq,
        quality,
        fs
    )

    return filtfilt(b, a, signal)


def preprocess_eeg(signal, fs=FS):
    """
    Complete EEG preprocessing pipeline.
    """

    signal = np.asarray(signal, dtype=float)

    # Remove DC offset
    cleaned = remove_dc(signal)

    # Remove 50 Hz electrical noise
    cleaned = notch_filter(
        cleaned,
        freq=50,
        fs=fs
    )

    # Keep EEG frequency range
    cleaned = bandpass_filter(
        cleaned,
        lowcut=0.5,
        highcut=45,
        fs=fs
    )

    return cleaned
