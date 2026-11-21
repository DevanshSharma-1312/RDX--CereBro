import numpy as np
from scipy.signal import welch


FS = 250


def calculate_band_power(freqs, psd, low, high):

    mask = (
        (freqs >= low) &
        (freqs < high)
    )

    if not np.any(mask):
        return 0.0

    return np.trapezoid(
        psd[mask],
        freqs[mask]
    )


def extract_brainwaves(signal, fs=FS):
    """
    Extract EEG band powers using Welch PSD.
    """

    freqs, psd = welch(
        signal,
        fs=fs,
        nperseg=min(len(signal), 512)
    )

    delta = calculate_band_power(
        freqs, psd,
        0.5, 4
    )

    theta = calculate_band_power(
        freqs, psd,
        4, 8
    )

    alpha = calculate_band_power(
        freqs, psd,
        8, 13
    )

    beta = calculate_band_power(
        freqs, psd,
        13, 30
    )

    gamma = calculate_band_power(
        freqs, psd,
        30, 45
    )

    total = (
        delta +
        theta +
        alpha +
        beta +
        gamma
    )

    # Relative powers in percentage
    if total > 0:

        delta_percent = delta / total * 100
        theta_percent = theta / total * 100
        alpha_percent = alpha / total * 100
        beta_percent = beta / total * 100
        gamma_percent = gamma / total * 100

    else:

        delta_percent = 0
        theta_percent = 0
        alpha_percent = 0
        beta_percent = 0
        gamma_percent = 0

    return {
        "delta": float(delta),
        "theta": float(theta),
        "alpha": float(alpha),
        "beta": float(beta),
        "gamma": float(gamma),

        "delta_percent": float(delta_percent),
        "theta_percent": float(theta_percent),
        "alpha_percent": float(alpha_percent),
        "beta_percent": float(beta_percent),
        "gamma_percent": float(gamma_percent)
    }
