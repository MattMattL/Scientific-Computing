import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import random as rand

class PresetButtons():

    # update the mode to Phase mode and print the right plot
    def phaseModeCallback(self, event):
        self.interface.mode = self.interface.Mode.PHASE
        self.interface.plotScreen.updatePlot()

    # update the mode to Frequency mode and print the right plot
    def freqModeCallback(self, event):
        self.interface.mode = self.interface.Mode.FREQUENCY
        self.interface.plotScreen.updatePlot()

    # update the mode to Adder mode and print the right plot
    def adderModeCallback(self, event):
        self.interface.mode = self.interface.Mode.ADD_NEW
        self.interface.plotScreen.updatePlot()


    ''' functions for drawing preset shapes: sin, sawtooth, triangle, square '''

    # preset sin wave with f=1
    def presetSinCallback(self, event):
        maxTime = self.interface.plotScreen.maxTime
        numPoints = self.interface.plotScreen.numPoints
        t = self.interface.plotScreen.arrTime

        # plot sin wave and update the screen
        self.interface.plotScreen.arrWave = np.sin(t*2*np.pi)
        self.interface.plotScreen.updatePlot()

    # preset square wave with f=1
    def presetSquareCallback(self, event):
        arrY = []

        # generate and save a square wave
        for t in self.interface.plotScreen.arrTime:
            val = 1 if int(2*t) % 2 == 0 else 0 # use modulus to find the right y value
            arrY.append(val)

        # update the original wave and update the plot
        self.interface.plotScreen.arrWave = arrY
        self.interface.plotScreen.updatePlot()

    # preset sawtooth wave with f=1
    def presetSawtoothCallback(self, event):
        arrY = []

        # generate sawtooth wave
        for t in self.interface.plotScreen.arrTime:
            arrY.append(t - int(t)) # increase y along t and drop by 1 at every integer t

        # update the original wave and update the plot
        self.interface.plotScreen.arrWave = arrY
        self.interface.plotScreen.updatePlot()

    # preset triangle wave with f=1
    def presetTriangleCallback(self, event):
        arrY = []

        #  generate triangle wave
        for t in self.interface.plotScreen.arrTime:
            # up-and-down figure using the floor function
            val = 4 * abs((t+0.25) - np.floor((t+0.25) + 1/2)) - 1
            arrY.append(val)

        # update the original wave and update the plot
        self.interface.plotScreen.arrWave = arrY
        self.interface.plotScreen.updatePlot()


    ''' callback functions for Add Noise and Reset '''

    # generates and adds random noise to the original wave
    def addNoiseCallback(self, event):
        # generate N random numbers in range [-0.5, 0.5)
        noise = np.random.random((self.interface.plotScreen.numPoints))/2 - 1/4

        # add to the existing wave and update the plot screen
        self.interface.plotScreen.arrWave += noise
        self.interface.plotScreen.updatePlot()

    # resets the wave to a constant line with y = 0
    def resetCallback(self, event):
        self.interface.plotScreen.arrWave = np.empty(self.interface.plotScreen.numPoints)
        self.interface.plotScreen.arrWave.fill(0)

        self.interface.plotScreen.updatePlot()

    def __init__(self, interfaceIn, plt):
        self.interface = interfaceIn
        self.plt = plt

        ''' add buttons for switching between different modes '''

        # add a button for switching into the Phase mode
        self.phaseAxes = self.plt.axes([0.455, 0.66, 0.06, 0.06])
        self.phaseHandler = widgets.Button(self.phaseAxes, 'PHASE')
        self.phaseHandler.on_clicked(self.phaseModeCallback)

        # add a button for switching into the Frequency mode
        self.freqAxis = self.plt.axes([0.455, 0.46, 0.06, 0.06])
        self.freqHandler = widgets.Button(self.freqAxis, 'FREQ')
        self.freqHandler.on_clicked(self.freqModeCallback)

        # Adder mode for generating and adding custom signals
        self.adderAxes = self.plt.axes([0.455, 0.26, 0.06, 0.06])
        self.adderHandler = widgets.Button(self.adderAxes, 'ADD')
        self.adderHandler.on_clicked(self.adderModeCallback)

        # add label above the buttons
        self.phaseAxes.annotate("-- Mode --", xy=(0.03, 1.7), xycoords='axes fraction')


        ''' add buttons for plotting preset functions '''

        # sin wave
        self.sinAxes = self.plt.axes([0.58, 0.2, 0.06, 0.08])
        self.sinHandler = widgets.Button(self.sinAxes, 'Sin')
        self.sinHandler.on_clicked(self.presetSinCallback)

        # square wave
        self.squareAxes = self.plt.axes([0.58, 0.1, 0.06, 0.08])
        self.squareHandler = widgets.Button(self.squareAxes, 'Square')
        self.squareHandler.on_clicked(self.presetSquareCallback)

        # sawtooth wave
        self.sawAxes = self.plt.axes([0.65, 0.1, 0.06, 0.08])
        self.sawHandler = widgets.Button(self.sawAxes, 'Saw')
        self.sawHandler.on_clicked(self.presetSawtoothCallback)

        # triangle wave
        self.tringleAxes = self.plt.axes([0.65, 0.2, 0.06, 0.08])
        self.triangleHandler = widgets.Button(self.tringleAxes, 'Triangle')
        self.triangleHandler.on_clicked(self.presetTriangleCallback)

        # add label above the preset buttons
        self.sinAxes.annotate("---------- Preset ----------", xy=(0, 1.4), xycoords='axes fraction')


        ''' functional buttons including Add Noise and Reset '''

        # button for adding randomised noise
        self.noiseAxes = self.plt.axes([0.77, 0.2, 0.06, 0.08])
        self.noiseHandler = widgets.Button(self.noiseAxes, 'Add Noise')
        self.noiseHandler.on_clicked(self.addNoiseCallback)

        # button for resetting the main wave to 0
        self.resetAxes = self.plt.axes([0.77, 0.1, 0.06, 0.08])
        self.resetHandler = widgets.Button(self.resetAxes, 'Reset')
        self.resetHandler.on_clicked(self.resetCallback)
