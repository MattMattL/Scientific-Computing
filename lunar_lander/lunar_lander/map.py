import numpy as np
import random as rand

from spaceship import Spaceship

class Map:

    plt = None
    elevation = [0]

    def __init__(self, plt):
        # save plt locally (no need to be passed every time)
        self.plt = plt

        # generate randomised landscape
        for x in range(200):
            # generate a random number following normal distribution with 'mean' and SD = 0.8
            mean = 0.5 * np.sin(x / 10) # alter the mean value with a certain period
            randNum = round(np.random.normal(size=1, loc=mean, scale=0.8)[0])

            # add the random number to the last elevation to generate a new elevation point
            possibleElevation = self.elevation[-1] + randNum

            # clamp the value in the range [-10, 10] and append
            self.elevation.append(self.clamp(possibleElevation, -10, 20))

    # clamps the value passed in given range
    def clamp(self, value, low, high):
        if low <= value <= high:
            return value;
        else:
            return low if value < low else high

    # draws the pre-randomised landscape on the screen
    def plot(self, screenWidth, centreX):
        x, y = [], []
        centreX = int(centreX)
        screenHalfX = int(screenWidth / 2)

        for i in range(centreX - screenHalfX - 1, centreX + screenHalfX + 5):
            x.append(i)
            y.append(self.elevation[i % len(self.elevation)])

        self.plt.plot(x, y, color='white', linestyle='-')

    # calculates and returns elevation at real x (since elevation points saved are discrete)
    def getElevationAt(self, x):
        # elevation is already known for integer x (return the raw value from array)
        if x == int(x):
            return self.elevation[int(x) % len(self.elevation)]

        # calculate the line equation using the two closes known elevation points around x
        size = len(self.elevation)

        x1, x2 = int(x), int(x) + 1
        y1, y2 = self.elevation[x1 % size], self.elevation[x2 % size]

        # return the elevation at x using the line equation
        return ((y2 - y1)/(x2 - x1)) * (x - x1) + y1
