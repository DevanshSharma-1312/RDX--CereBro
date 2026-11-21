import serial
import time


class EEGSerialReader:
    def __init__(self, port="COM7", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        print(f"Connecting to ESP32 on {self.port}...")

        self.ser = serial.Serial(
            self.port,
            self.baudrate,
            timeout=1
        )

        time.sleep(2)

        print("Connected successfully!")

    def read_sample(self):
        """
        Reads one EEG sample from ESP32.
        Expected serial format:
        2048
        2051
        2039
        """

        if self.ser is None:
            raise Exception("Serial connection not initialized.")

        try:
            line = self.ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if line:
                value = float(line)
                return value

        except ValueError:
            # Ignore non-numeric messages
            return None

        except Exception as e:
            print("Serial error:", e)
            return None

        return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")
