# SinewaveApp

Real-time Sinewave Plotting and Data Saving with PyQt5
This project consists of two Python scripts, sinewave_generator.py and SinewaveApp.py, which together form a simple, user-friendly GUI application using PyQt5 that allows users to plot a real-time, randomly generated sinewave and save the data at specified intervals.

sinewave_generator.py
This script defines a SinewaveGenerator class that generates a sinewave signal at a specified frequency and sample rate. It also stores the sinewave data and timestamps and has methods for generating data and updating the frequency.

SinewaveApp.py
This script defines a SinewaveApp class that creates the GUI application using PyQt5. The GUI consists of a main window with a button to start and stop the sinewave plotting, a frequency slider, and a plot window. Upon clicking the button, the plot window starts displaying a randomly generated, real-time sinewave. The button starts an independent script that will run the sinewave function and generate data. The sinewave data is saved to a numpy file every 1 second, and all data from the sinewave is saved to a separate numpy file every 5 minutes.

Dependencies
    PyQt5
    numpy
    matplotlib

Usage
To run the sinewave app, simply run the SinewaveApp.py script:

    python SinewaveApp.py
    
The sinewave generator can also be used independently of the GUI app. To do this, import the SinewaveGenerator class and create an instance of it with a specified frequency and sample rate:

    from sinewave_generator import SinewaveGenerator

    # Create a SinewaveGenerator with a frequency of 1 Hz and sample rate of 100 samples/s
    sinewave_generator = SinewaveGenerator(frequency=1, sample_rate=100)

    # Generate a new sinewave value
    sinewave_value = sinewave_generator.generate_data()

    # Update the frequency to 2 Hz
    sinewave_generator.update_frequency(2)