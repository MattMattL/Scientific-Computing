import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class ScalerKnobs():

    # called when the horizontal-scaler slider is updated
    def horizontalScaleCallback(self, val):
        if self.interface.mode == self.interface.Mode.PHASE:
            self.interface.plotScreen.horPhaseScaler = val
            self.interface.plotScreen.updatePlot()
        
        elif self.interface.mode == self.interface.Mode.FREQUENCY:
            self.interface.plotScreen.horFreqScaler = val
            self.interface.plotScreen.updatePlot()

    # called when the vertical-scaler slider is updated
    def verticalScaleCallback(self, val):
        if self.interface.mode == self.interface.Mode.PHASE:
            self.interface.plotScreen.verPhaseScaler = val
            self.interface.plotScreen.updatePlot()
        
        elif self.interface.mode == self.interface.Mode.FREQUENCY:
            self.interface.plotScreen.verFreqScaler = val
            self.interface.plotScreen.updatePlot()

    # deletes and re-draws the indicator at new position
    def updateHorizontalKnob(self, val):
        # calculate new position of the knob
        theta = -np.pi/6 * val + 17*np.pi/12

        # update x and y value
        self.horKnobHandler.set_xdata(np.cos(theta))
        self.horKnobHandler.set_ydata(np.sin(theta))

    # deletes and re-draws the indicator at new position
    def updateVerticalKnob(self, val):
        # calculate new position of the knob
        theta = -np.pi/6 * val + 17*np.pi/12

        # update x and y value
        self.verKnobHandler.set_xdata(np.cos(theta))
        self.verKnobHandler.set_ydata(np.sin(theta))

    def __init__(self, interfaceIn, plt):
        # save things locally to use later
        self.interface = interfaceIn
        self.plt = plt

        # add a slider, representing a "knob", for adjusting left windowing limit
        self.horAxes = self.plt.axes([0.58, 0.7, 0.06, 0.02])
        self.horHandler = widgets.Slider(self.horAxes, '◁ ▷ ', 1, 10, valinit=1, color='white')
        self.horHandler.on_changed(self.horizontalScaleCallback)
        self.horHandler.valtext.set_visible(False)

        # add a slider, representing a "knob", for adjusting left windowing limit
        self.verAxes = self.plt.axes([0.68, 0.7, 0.06, 0.02])
        self.verHandler = widgets.Slider(self.verAxes, '', 1, 10, valinit=1, color='white')
        self.verHandler.on_changed(self.verticalScaleCallback)
        self.verHandler.valtext.set_visible(False)

        # separately add the up & down arrows as it does not fit in a single line
        self.verAxes.annotate("△\n▽", xy=(-0.3, -0.6), xycoords='axes fraction')

        # add label above the scaler knobs
        self.horAxes.annotate("--------------  Scale --------------", xy=(0, 10), xycoords='axes fraction')

        # x, y and theta for drawing a "knob"
        theta = np.linspace(0, 2*np.pi, 80)
        x = 1.4 * np.cos(theta)
        y = 1.4 * np.sin(theta)

        # draw graphics for the left windowing knob
        self.horKnob = self.plt.axes([0.58, 0.74, 0.7/12, 0.7/5])
        self.horKnob.axis('off')
        self.horKnob.plot(x, y, color='black', linewidth=0.8)
        self.horKnobHandler, = self.horKnob.plot(0, 0, marker='o', color='black', markersize=4)
        self.updateHorizontalKnob(1)

        # draw graphics for the right windowing knob
        self.verKnob = self.plt.axes([0.68, 0.74, 0.7/12, 0.7/5])
        self.verKnob.axis('off')
        self.verKnob.plot(x, y, color='black', linewidth=0.8)
        self.verKnobHandler, = self.verKnob.plot(0, 0, marker='o', color='black', markersize=4)
        self.updateVerticalKnob(1)