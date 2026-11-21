import time
import numpy as np

from serial_reader import EEGSerialReader
from preprocessing import preprocess_eeg
from band_analysis import extract_brainwaves


# =========================
# CONFIGURATION
# =========================

SERIAL_PORT = "COM11"
BAUD_RATE = 115200

SAMPLE_RATE = 250

WINDOW_SECONDS = 4

WINDOW_SIZE = SAMPLE_RATE * WINDOW_SECONDS


# =========================
# MAIN
# =========================

def main():

    print("=" * 50)
    print("REAL-TIME EEG PROCESSING SYSTEM")
    print("=" * 50)

    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print(f"Window Size: {WINDOW_SIZE} samples")
    print(f"Analysis Window: {WINDOW_SECONDS} seconds")

    print()

    # Connect ESP32

    reader = EEGSerialReader(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE
    )

    reader.connect()

    buffer = []

    try:

        while True:

            sample = reader.read_sample()

            if sample is not None:

                buffer.append(sample)

                print(
                    f"\rSamples: {len(buffer)}/{WINDOW_SIZE}",
                    end=""
                )

            # When buffer reaches analysis size

            if len(buffer) >= WINDOW_SIZE:

                print("\n")
                print("Processing EEG window...")

                signal = np.array(buffer)

                # =========================
                # PREPROCESS
                # =========================

                clean_signal = preprocess_eeg(
                    signal,
                    fs=SAMPLE_RATE
                )

                # =========================
                # EXTRACT BRAIN WAVES
                # =========================

                bands = extract_brainwaves(
                    clean_signal,
                    fs=SAMPLE_RATE
                )

                # =========================
                # DISPLAY RESULTS
                # =========================

                print()
                print("BRAIN WAVE ANALYSIS")
                print("-" * 40)

                print(
                    f"Delta : {bands['delta_percent']:.2f}%"
                )

                print(
                    f"Theta : {bands['theta_percent']:.2f}%"
                )

                print(
                    f"Alpha : {bands['alpha_percent']:.2f}%"
                )

                print(
                    f"Beta  : {bands['beta_percent']:.2f}%"
                )

                print(
                    f"Gamma : {bands['gamma_percent']:.2f}%"
                )

                print("-" * 40)

                # Clear buffer for next window

                buffer = []

    except KeyboardInterrupt:

        print("\nStopping EEG processing...")

    finally:

        reader.close()


if __name__ == "__main__":
    main()
