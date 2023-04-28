# Import our sinewave generator
from sinewave_generator import SinewaveGenerator

# Import required libraries
import os
import sys
import numpy as np
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QSlider, QLabel
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Constants
SAMPLE_RATE = 100    # samples / s

# Function to create a data folder if it does not exist
def create_data_folder():
    if not os.path.exists('data'):
        os.makedirs('data')

# Main Application Class
class SinewaveApp(QMainWindow):
    # Constructor
    def __init__(self):
        super().__init__()
        # Create a data folder if it doesn't exist
        create_data_folder()
        # Variable to check if the plot is running
        self.is_plotting = False

        # Window Title
        self.title = 'Real-time Sinewave Plotting and Data Saving with PyQt5'
        # Initialize User Interface
        self.init_ui()

    # Function to initialize the UI
    def init_ui(self):
        # Set Window Title and Position
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Start Button
        self.start_button = QPushButton('Start Sinewave')
        self.start_button.clicked.connect(self.toggle_sinewave)
        layout.addWidget(self.start_button)

        # Frequency Label
        self.freq_label = QLabel()
        self.freq_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.freq_label)

        # Frequency Slider
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(50)
        self.freq_slider.setValue(10)
        self.freq_slider.valueChanged.connect(self.freq_changed)
        layout.addWidget(self.freq_slider)

        # Canvas for Plotting
        self.canvas = PlotCanvas(self, width=8, height=4)  # Pass self (SinewaveApp instance) to PlotCanvas
        layout.addWidget(self.canvas)

        # Set initial frequency
        self.freq_changed(10)

        # Set the layout to the main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Event handler for frequency slider
    def freq_changed(self, value):
        self.freq_label.setText(f'Frequency: {value} Hz')
        self.canvas.freq = value
        # Update the frequency in the SinewaveGenerator
        self.canvas.sinewave_generator.update_frequency(value)

    # Function to start or stop the sinewave
    def toggle_sinewave(self):
        if self.is_plotting:
            self.stop_sinewave()
        else:
            self.start_sinewave()

    # Function to start the sinewave
    def start_sinewave(self):
        self.start_button.setText('Stop Sinewave')
        self.is_plotting = True
        self.canvas.start_plotting()

    # Function to stop the sinewave
    def stop_sinewave(self):
        self.start_button.setText('Start Sinewave')
        self.is_plotting = False
        self.canvas.stop_plotting()

    # Event handler for closing the application
    def closeEvent(self, event):
        self.canvas.stop_plotting()
        event.accept()

# Class for the plotting canvas
class PlotCanvas(FigureCanvas):
    # Constructor
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # Initialize parent class
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # Store the reference to the SinewaveApp instance
        self.main_app = parent  

        # Initialize the sinewave generator
        self.sinewave_generator = SinewaveGenerator(sample_rate=SAMPLE_RATE)

        self.max_data_points = SAMPLE_RATE * 60 * 5  # Store data of last 5 minutes

        # Initialize the sinewave data and frequency
        self.freq = 1

    # Function to start plotting
    def start_plotting(self):
        # Reset data
        self.sinewave_generator.sinewave_data = []
        self.sinewave_generator.timestamps = []
        
        self.sinewave_generator.update_frequency(self.freq)

        # Set up timers for plot update and data saving
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        # Timer for generating sinewave data
        self.sinewave_gen_timer = QTimer()
        self.sinewave_gen_timer.timeout.connect(self.sinewave_generator.generate_data)
        self.sinewave_gen_timer.start(int(1000 / self.sinewave_generator.sample_rate))  # Adjust the interval to match the sample rate

        # Timer for saving data every second
        self.save_data_timer = QTimer()
        self.save_data_timer.timeout.connect(self.save_data)
        self.save_data_timer.start(1000)

        # Timer for saving all data every 5 minutes
        self.save_all_data_timer = QTimer()
        self.save_all_data_timer.timeout.connect(self.save_all_data)
        self.save_all_data_timer.start(300000)

    # Function to stop plotting
    def stop_plotting(self):
        # Stop all timers
        self.timer.stop()
        self.sinewave_gen_timer.stop()
        self.save_data_timer.stop()
        self.save_all_data_timer.stop()

    # Function to save data
    def save_data(self):
        current_time = time.strftime("%Y%m%d-%H%M%S")
        last_second_data = self.sinewave_generator.sinewave_data[-SAMPLE_RATE:]  # Get last second data
        np.save(f'data/sinewave_data_{current_time}.npy', last_second_data)

    # Function to save all data
    def save_all_data(self):
        current_time = time.strftime("%Y%m%d-%H%M%S")
        np.save(f'data/sinewave_data_all_{current_time}.npy', self.sinewave_generator.sinewave_data)

    # Function to update the plot
    def update_plot(self):
        # Calculate the number of samples in the most recent 3 seconds
        recent_samples = self.sinewave_generator.sample_rate * 3

        # Get the most recent 3 seconds of data
        recent_sinewave_data = self.sinewave_generator.sinewave_data[-recent_samples:]
        recent_timestamps = self.sinewave_generator.timestamps[-recent_samples:]

        # Plot the recent sinewave data
        self.axes.clear()
        self.axes.plot(recent_timestamps, recent_sinewave_data, 'b-')
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Amplitude')
        self.draw()

# Main function
if __name__ == '__main__':
    # Create a Qt Application
    app = QApplication(sys.argv)

    # Create and show the SinewaveApp
    ex = SinewaveApp()
    ex.show()

    # Run the main Qt loop
    sys.exit(app.exec_())

