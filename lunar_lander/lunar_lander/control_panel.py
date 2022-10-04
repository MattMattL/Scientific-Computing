import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
import math

class ControlPanel():

    '''
    Uninitialised Global Variables
    ------------------------------
    plt
    landscape
    lander
    '''

    # angles for drawing the control panel
    minAngle = -np.pi / 6 
    maxAngle = 7/6 * np.pi

    def __init__(self, plt, landscape, lander):
        # save parameters locally
        self.plt = plt
        self.landscape = landscape
        self.lander = lander

    # clamps the value passed in given range
    def clamp(self, value, low, high):
        if low <= value <= high:
            return value;
        else:
            return low if value < low else high

    # draws a meter panel at a specified location and a value
    def plotPanel(self, offsetX, value, low, high):
        # plot 4/3 of a circle for the display outline
        theta = np.linspace(self.minAngle, self.maxAngle, 30)
        self.plt.plot(offsetX + np.cos(theta), np.sin(theta), 'w-')

        # calculate the angle for the indicator needle
        angle = (-np.pi / 6) + (8/6 * np.pi) * (high - value)/(high - low)
        angle = self.clamp(angle, -np.pi/6, 7/6 * np.pi)

        # plot the red needle
        x = [offsetX, offsetX + 0.9*np.cos(angle)]
        y = [0, 0.9*np.sin(angle)]
        
        self.plt.plot(x, y, 'r-')

    # calculates current elevation and passes the info to 'plotPanel'
    def plotAltitude(self):
        elevation = self.landscape.getElevationAt(self.lander.pos.x)
        altitude = self.lander.pos.y - elevation

        self.plt.annotate('$h$ = {:.1f} $m$'.format(altitude), xy=(0.02, 0), xycoords='axes fraction', color='white')
        self.plotPanel(1.5, self.lander.pos.y, elevation, 120)

    # formats and prints vertical velocity and passes the info to 'plotPanel'
    def plotSpeed(self):
        # plot a warning bar at the threshold velocity
        angle = (-np.pi / 6) + 13/15 * (8/6 * np.pi) # min + ratio * interval
        x = [5, 5 + 0.9*np.cos(angle)]
        y = [0, 0.9*np.sin(angle)]
        self.plt.plot(x, y, color='white', linestyle='--', linewidth=0.5)
        
        # call 'plotPanel' to draw the rest of the meter
        formatted = '$v_y$ = {:.1f} $m/s$'.format(-self.lander.vel.y)
        self.plt.annotate(formatted, xy=(0.24, 0), xycoords='axes fraction', color='white')

        self.plotPanel(5, -self.lander.vel.y, 0, 15)

    # formats and prints vertical acceleration and passes the info to 'plotPanel'
    def plotAcceleration(self):
        formatted = '$a_y$ = {:.1f} $m/s^2$'.format(-self.lander.acc.y)
        self.plt.annotate(formatted, xy=(0.46, 0), xycoords='axes fraction', color='white')

        self.plotPanel(8.5, self.lander.acc.y, -1, 2)

    # calculates fuel left and passes the info to 'plotPanel'
    def plotFuelMeter(self):
        fuelPercentage = 100 * self.lander.fuel / self.lander.MAX_FUEL
        formatted = 'Fuel = {:5.1f}%'.format(fuelPercentage)
        self.plt.annotate(formatted, xy=(0.7, 0), xycoords='axes fraction', color='white')

        self.plotPanel(12, self.lander.fuel, 0, self.lander.MAX_FUEL)

    # draws 4 meters on the control panel axes (altitude, speed, acceleration, fuel)
    def plot(self):
        self.plotAltitude()
        self.plotSpeed()
        self.plotAcceleration()
        self.plotFuelMeter()
