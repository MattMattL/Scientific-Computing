import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from typing import Tuple

# Function that plots sine
def sinf(t:np.ndarray, f:float) -> np.ndarray:
    # return an array of sin(2πft) for varying t
    return np.sin(2 * np.pi * f * t)

# Performs Fourier Transformation and returns arrays of amplitude and frequency
def fourier_func(amplitude:np.ndarray, t_max:float) -> Tuple[np.ndarray, np.ndarray]:
    N = len(amplitude)

    # frequency is a function of time (dt/T * n)
    frequency = [n/t_max for n in range(N)]

    # calculate the output array in the frequency space
    fourier = [sum(amplitude[t] * np.exp(-2j*np.pi/N * t*k) for t in range(N)) for k in range(N)]
    # power is |X(k)|^2
    power = [x*x.conjugate()/N for x in fourier]

    return power, frequency

# Fourier transfomation function that returns X(k) rather than |X(k)|^2
def fourier_transform(amplitude:np.ndarray, t_max:float) -> Tuple[np.ndarray, np.ndarray]:
    N = len(amplitude)

    # frequency is a function of time (dt/T * n)
    frequency = [n/t_max for n in range(N)]

    # calculate the output array in the frequency space
    fourier = [sum(amplitude[t] * np.exp(-2j*np.pi/N * t*k) for t in range(N)) for k in range(N)]

    return fourier, frequency

# Inverse fourier transformation function. Returns time[t] and x[t] (inverse fourier)
def inverse_fourier_transform(amplitude:np.ndarray, freq_max:float) -> Tuple[np.ndarray, np.ndarray]:
    N = len(amplitude)

    # time intervals
    time = [t/freq_max for t in range(N)]

    # calculate amplitude the time space
    inverse_fourier = [1./N * sum(amplitude[k] * np.exp(2j*np.pi/N * t*k) for k in range(N)) for t in range(N)]

    return inverse_fourier, time


"""Basic oscilloscope figure layout with signal window, Fourier power window, 
    frequency slider and exit button
"""

# Event when exit button is pressed
def exit_button(event):
    plt.close('all')

# Update the signal and power plots when the frequency slider is moved    
def freq_slider(val):
    global t, signal_line_handle, fourier_line_handle
    signal_amplitude = sinf(t, val)
    signal_line_handle.set_ydata(signal_amplitude)
    power, freq = fourier_func(signal_amplitude,t_max)
    fourier_line_handle.set_ydata(power)
    fourier_line_handle.set_xdata(freq)
    plt.draw()
    
if __name__ == "__main__":
    # Creates oscilloscope figure window 
    fig = plt.figure(figsize = (12,5))
    signal_ax = plt.axes([0.05, 0.4, 0.4, 0.4])
    # Labels axes and title signal graph
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('Signal')
    # Sets initial axis limits
    signal_ax.set_xlim([0, 3])
    signal_ax.set_ylim([-2, 2])

    # Initial values for no. of points, frequency and time (t_max)
    initial_points = 300
    initial_sin_freq = 1.
    t_max = 3.

    # Creates initial time value array
    t = np.linspace(0, t_max, initial_points)
    """
    Remove the line below and uncomment the next one when you have a signal return from the sinf function above
    """
    signal_amplitude = np.zeros(initial_points)
    # signal_amplitude = sinf(t , initial_sin_freq)
    signal_line_handle, = signal_ax.plot(t , signal_amplitude)

    # Create Exit Button
    exit_ax = plt.axes([0.8, 0.15, 0.05, 0.05])
    close_button = widgets.Button(exit_ax, 'Exit')
    close_button.on_clicked(exit_button)

    # Create Frequency Slider
    # Placement of frequency slider
    freq_slider_ax = plt.axes([0.15, 0.2, 0.25, 0.03])
    # Widget for frequency slider
    frequency_slider = widgets.Slider(freq_slider_ax, 'Frequency', 0.1, 5, \
                    valinit= initial_sin_freq)
    # Calls function to change plot when frequency slider is changed
    frequency_slider.on_changed(freq_slider)

    #sets up power spectrum plot
    fourier_ax = plt.axes([0.55, 0.4, 0.4, 0.4])
    plt.xlabel('Frequency (per sec)')
    plt.ylabel('Amplitude')
    plt.title('Power spectrum')

    """
    Remove the line below and uncomment the following two lines when you have 
    a power return from fourier_func function.
    """
    fourier_line_handle, = plt.plot([0.,0.])
    # power, freq = fourier_func(signal_amplitude,t_max)
    # fourier_line_handle, = plt.plot(freq, power)
    fourier_ax.set_xlim([0, 7])
    fourier_ax.set_ylim([0, 150])

    plt.show()
