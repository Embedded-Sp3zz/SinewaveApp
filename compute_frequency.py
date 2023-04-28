import numpy as np

def compute_frequency(data, sample_rate):
    """
    Compute the frequency of a signal using the FFT.

    Args:
    data: A list or numpy array containing the signal data.
    sample_rate: The sample rate of the signal in Hz.

    Returns:
    The frequency of the signal in Hz.
    """
    # Compute FFT
    fft_vals = np.fft.rfft(data)

    # Compute the frequencies associated with the FFT values
    fft_freq = np.fft.rfftfreq(len(data), 1.0/sample_rate)

    # Find the peak frequency: we can focus on only the positive frequencies
    peak_freq = fft_freq[np.argmax(np.abs(fft_vals))]

    return peak_freq
