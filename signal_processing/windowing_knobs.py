import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class WindowingKnobs:

    # saves and updates the new value of the left windowing limit
    def leftSliderCallback(self, percent):
        # windowing in Phase mode
        if self.interface.mode == self.interface.Mode.PHASE:
            self.interface.plotScreen.leftPhaseMaskPercent = percent
            self.interface.plotScreen.updatePlot()
        # windowing in Frequency mode (= filtering)
        elif self.interface.mode == self.interface.Mode.FREQUENCY:
            self.interface.plotScreen.leftFreqMaskPercent = percent
            self.interface.plotScreen.updatePlot()

    # saves and updates the new value of the right windowing limit
    def rightSliderCallback(self, percent):
        # windowing in Phase mode
        if self.interface.mode == self.interface.Mode.PHASE:
            self.interface.plotScreen.rightPhaseMaskPercent = percent
            self.interface.plotScreen.updatePlot()
        # windowing in Frequency mode (= filtering)
        elif self.interface.mode == self.interface.Mode.FREQUENCY:
            self.interface.plotScreen.rightFreqMaskPercent = percent
            self.interface.plotScreen.updatePlot()

    def updateLeftKnob(self, percent):
        # calculuate new position of the knob
        theta = -3*np.pi/2 * percent/100 + 5*np.pi/4

        # update x and y value
        self.leftKnobHandler.set_xdata(np.cos(theta))
        self.leftKnobHandler.set_ydata(np.sin(theta))

    def updateRightKnob(self, percent):
        # calculuate new position of the knob
        theta = -3*np.pi/2 * percent/100 + 5*np.pi/4

        # update x and y value
        self.rightKnobHandler.set_xdata(np.cos(theta))
        self.rightKnobHandler.set_ydata(np.sin(theta))

    def __init__(self, interfaceIn, plt):
        self.interface = interfaceIn
        self.plt = plt

        # add a slider, representing a "knob", for adjusting left windowing limit
        self.leftAxes = self.plt.axes([0.78, 0.7, 0.06, 0.02])
        self.leftHandler = widgets.Slider(self.leftAxes, 'L ', 0, 100, valinit=0, color='white')
        self.leftHandler.on_changed(self.leftSliderCallback)
        self.leftHandler.valtext.set_visible(False)

        # add a slider, representing a "knob", for adjusting right windowing limit
        self.rightAxes = self.plt.axes([0.88, 0.7, 0.06, 0.02])
        self.rightHandler = widgets.Slider(self.rightAxes, 'R ', 0, 100, valinit=100, color='white')
        self.rightHandler.on_changed(self.rightSliderCallback)
        self.rightHandler.valtext.set_visible(False)

        # add a lable above the knobs
        self.leftAxes.annotate("-------------  Masks -------------", xy=(0, 10), xycoords='axes fraction')

        # x, y and theta for drawing a "knob"
        theta = np.linspace(0, 2*np.pi, 80)
        x = 1.4 * np.cos(theta)
        y = 1.4 * np.sin(theta)

        # draw graphics for the left windowing knob
        self.leftKnob = self.plt.axes([0.78, 0.74, 0.7/12, 0.7/5])
        self.leftKnob.axis('off')
        self.leftKnob.plot(x, y, color='black', linewidth=0.8)
        self.leftKnobHandler, = self.leftKnob.plot(0, 0, marker='o', color='blue', markersize=4)
        self.updateLeftKnob(0)

        # draw graphics for the right windowing knob
        self.rightKnob = self.plt.axes([0.88, 0.74, 0.7/12, 0.7/5])
        self.rightKnob.axis('off')
        self.rightKnob.plot(x, y, color='black', linewidth=0.8)
        self.rightKnobHandler, = self.rightKnob.plot(0, 0, marker='o', color='grey', markersize=4)
        self.updateRightKnob(100)
