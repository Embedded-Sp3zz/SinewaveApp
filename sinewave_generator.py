import numpy as np
import time

class SinewaveGenerator:
    def __init__(self, frequency=1, sample_rate=100):
        self.freq = frequency
        self.sample_rate = sample_rate  # samples per second
        self.time = 0
        self.sinewave_data = []  # Store the sinewave data
        self.timestamps = []  # Store the timestamps

    def generate_data(self):
        # Calculate the time step
        dt = 1.0 / self.sample_rate

        # Generate a new sinewave value
        y = np.sin(self.freq * 2 * np.pi * self.time)

        # Append to the data list and timestamps
        self.sinewave_data.append(y)
        self.timestamps.append(self.time)

        # Keep data points within max_data_points
        if len(self.sinewave_data) > self.sample_rate * 5 * 60:
            self.sinewave_data.pop(0)
            self.timestamps.pop(0)

        # Update time
        self.time += dt

        return y

    def update_frequency(self, frequency):
        self.freq = frequency
