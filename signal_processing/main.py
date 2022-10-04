'''
Scientific Computing - Signal Processing

Start Date      2 Nov 2021
Due Date        8 Nov 2021

    Description

This virtual oscilloscope can handle waves and fourier transformation.


    Extra Features

- Buttons for adjusting the number of plotting points

- Three different display modes (Phase, Frequency and Adder mode)

- Windowing feature using two dials (works in both phase and k-space).

- Adder mode where the user can add a new wave to the existing one with variable
  frequency, amplitude and initial phase offset.

- Preset waves including sin, sawtooth, triangle and square wave.

- Random noise and a reset button.

- Vertical and horizontal scaler (works in both phase and k-space)

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from plot_screen import PlotScreen
from windowing_knobs import WindowingKnobs
from points_buttons import PointsButtons
from preset_buttons import PresetButtons
from new_wave_knobs import NewWaveKnobs
from information_panel import InformationPanel
from scaler_knobs import ScalerKnobs

class Oscilloscope:

    # three modes for plotting different information on the screen
    class Mode:
        PHASE = 1
        FREQUENCY = 2
        ADD_NEW = 3

    # default is Phase mode
    mode = Mode.PHASE
        
    # initialise figure, axes and other callback functions
    def __init__(self):
        # initialise the figure and set backgournd color to a slightly faded whtie
        fig = plt.figure(figsize = (12,5), facecolor=(0.9, 0.9, 0.9))
        fig.canvas.set_window_title("Ozzy the Osilloscope")

        # declare the screen, buttons and dials.
        # this initialises the classes' callback functions.
        self.plotScreen = PlotScreen(self, plt)
        self.windowingKnobs = WindowingKnobs(self, plt)
        self.pointsButtons = PointsButtons(self, plt)
        self.presetButtons = PresetButtons(self, plt)
        self.newWaveKnobs = NewWaveKnobs(self, plt)
        self.informationPanel = InformationPanel(self, plt)
        self.scalerKnobs = ScalerKnobs(self, plt)

        # initailly show the graphics.
        # updatings the graphics is done in the callback functions in PlotScreen.
        plt.show()

# execute only if ran directly
if __name__ == "__main__":
    oscilloscope = Oscilloscope()
