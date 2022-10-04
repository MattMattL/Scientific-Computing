import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class NewWaveKnobs():

    # saves and updates the new frequency value for generating a new wave (in percentage)
    def frequencyCallback(self, val):
        self.interface.plotScreen.newFrequencyPercent = val
        
        # update the plot screen if required immediately
        if self.interface.mode == self.interface.Mode.ADD_NEW:
            self.interface.plotScreen.updatePlot()
        
        # update the graphics of the knob position
        self.updateFreqKnob(val)

    # saves and updates the new amplitude (scaler)
    def amplitudeCallback(self, val):
        self.interface.plotScreen.newAmplitudeModifier = val
        
        # update the plot screen if required immediately
        if self.interface.mode == self.interface.Mode.ADD_NEW:
            self.interface.plotScreen.updatePlot()
        
        # update the graphics of the knob position
        self.updateAmpKnob(val)

    # saves and updates the new offset (in percentage)
    def offsetCallback(self, val):
        self.interface.plotScreen.newOffsetPercent = val
        
        # update the plot screen if required immediately
        if self.interface.mode == self.interface.Mode.ADD_NEW:
            self.interface.plotScreen.updatePlot()
        
        # update the graphics of the knob position
        self.updateOffsetKnob(val)

    # callback function for the Confirm button
    def addButtonCallback(self, event):
        # add the newly generated wave to the existing wave and update the plot
        self.interface.plotScreen.arrWave += self.interface.plotScreen.arrNewWave
        self.interface.plotScreen.updatePlot()


    # updates the position of the frequency knob
    def updateFreqKnob(self, val):
        # calculate the new position of the indicator dot in radian
        theta = -3*np.pi/2 * val/100 + 5*np.pi/4

        # update x and y value
        self.freqKnobHandler.set_xdata(np.cos(theta))
        self.freqKnobHandler.set_ydata(np.sin(theta))

    # updates the position of the amplitude knob
    def updateAmpKnob(self, val):
        # calculate the new position of the indicator dot in radian
        theta = -3*np.pi/2 * val/2 + 5*np.pi/4

        # update x and y value
        self.ampKnobHandler.set_xdata(np.cos(theta))
        self.ampKnobHandler.set_ydata(np.sin(theta))

    # updates the position of the offset knob
    def updateOffsetKnob(self, val):
        # calculate the new position of the indicator dot in radian
        theta = -3*np.pi/2 * val/100 + (5*np.pi/4 - 3*np.pi/4)

        # update x and y value
        self.offsetKnobHandler.set_xdata(np.cos(theta))
        self.offsetKnobHandler.set_ydata(np.sin(theta))

    def __init__(self, interfaceIn, plt):
        # save frequently used variables locally
        self.interface = interfaceIn
        self.plt = plt

        # set slider axes and callback function for the frequency knob
        self.freqAxes = self.plt.axes([0.58, 0.42, 0.06, 0.02])
        self.freqHandler = widgets.Slider(self.freqAxes, 'Freq ', 0.001, 100, valinit=10, valfmt='%3d%%', color='white')
        self.freqHandler.on_changed(self.frequencyCallback)
        self.freqHandler.valtext.set_visible(False)

        # set slider axes and callback function for the amplitude knob
        self.ampAxes = self.plt.axes([0.68, 0.42, 0.06, 0.02])
        self.ampHandler = widgets.Slider(self.ampAxes, 'Amp ', 0, 2, valinit=0.25, valfmt='%.1f', color='white')
        self.ampHandler.on_changed(self.amplitudeCallback)
        self.ampHandler.valtext.set_visible(False)

        # set slider axes and callback function for the offset knob
        self.offsetAxes = self.plt.axes([0.78, 0.42, 0.06, 0.02])
        self.offsetHandler = widgets.Slider(self.offsetAxes, 'Offset', -50, 50, valinit=0, valfmt='%3d%%', color='white')
        self.offsetHandler.on_changed(self.offsetCallback)
        self.offsetHandler.valtext.set_visible(False)

        # a button for confirming the new wave (add the custom generated wave to the existing one)
        self.addButtonAxes = self.plt.axes([0.87, 0.47, 0.06, 0.08])
        self.addButtonHandler = widgets.Button(self.addButtonAxes, 'Confirm')
        self.addButtonHandler.on_clicked(self.addButtonCallback)

        # add a label above the buttons
        label = "------------------------  New Wave Config (ADD) ------------------------"
        self.freqAxes.annotate(label, xy=(0, 9), xycoords='axes fraction')

        # x, y and theta for drawing a circle representing a knob
        theta = np.linspace(0, 2*np.pi, 80)
        x = 1.4 * np.cos(theta)
        y = 1.4 * np.sin(theta)

        # add axes for drawing a circle representing the frequency knob
        self.freqKnob = self.plt.axes([0.589, 0.46, 0.5/12, 0.5/5])
        self.freqKnob.axis('off')
        self.freqKnob.plot(x, y, color='black', linewidth=0.8)
        self.freqKnobHandler, = self.freqKnob.plot(0, 0, marker='.', color='black', markersize=4)
        self.updateFreqKnob(10)

        # add axes for drawing a circle representing the amplitude knob
        self.ampKnob = self.plt.axes([0.689, 0.46, 0.5/12, 0.5/5])
        self.ampKnob.axis('off')
        self.ampKnob.plot(x, y, color='black', linewidth=0.8)
        self.ampKnobHandler, = self.ampKnob.plot(0, 0, marker='.', color='black', markersize=4)
        self.updateAmpKnob(0.25)

        # add axes for drawing a circle representing the offset knob
        self.offsetKnob = self.plt.axes([0.789, 0.46, 0.5/12, 0.5/5])
        self.offsetKnob.axis('off')
        self.offsetKnob.plot(x, y, color='black', linewidth=0.8)
        self.offsetKnobHandler, = self.offsetKnob.plot(0, 0, marker='.', color='black', markersize=4)
        self.updateOffsetKnob(0)
