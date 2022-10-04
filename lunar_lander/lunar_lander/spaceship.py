import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
import math

class Spaceship():

    ROTATION_OFFSET = 2
    MAX_FUEL = 50

    plt = None
    fuel = MAX_FUEL

    def __init__(self, plt):
        # save plt locally (no need to be passed every time)
        self.plt = plt

    # updates velocity and and position. called every frame
    def tick(self, deltaTime):
        # Newton's equation of motion
        self.vel.x += self.acc.x * deltaTime
        self.vel.y += self.acc.y * deltaTime

        self.pos.x += self.vel.x * deltaTime
        self.pos.y += self.vel.y * deltaTime

    # handles transforming and plotting a line between two given points
    def plotLine(self, x1, x2, y1, y2):
        # offset y values so that the (rough) centre of the ship is around the origin
        y1 -= self.ROTATION_OFFSET
        y2 -= self.ROTATION_OFFSET

        # apply rotation transformations
        x1, x2, y1, y2 = \
                x1*np.cos(self.rad) - y1*np.sin(self.rad) + self.pos.x, \
                x2*np.cos(self.rad) - y2*np.sin(self.rad) + self.pos.x, \
                x1*np.sin(self.rad) + y1*np.cos(self.rad) + self.pos.y, \
                x2*np.sin(self.rad) + y2*np.cos(self.rad) + self.pos.y

        # move back to the original basis
        y1 += self.ROTATION_OFFSET
        y2 += self.ROTATION_OFFSET

        # plot the line
        self.plt.plot([x1, x2], [y1, y2], color='white', linestyle='-', linewidth=0.8)

    # draws the spaceship at its new position
    def plot(self, thrust):
        # engine gas(?)
        theta = np.linspace(np.pi, 2 * np.pi, 90)
        
        x = 0.3 * np.cos(theta)
        y = (thrust**2 * np.sin(theta) / 2) - self.ROTATION_OFFSET

        x, y = x*np.cos(self.rad) - y*np.sin(self.rad) + self.pos.x, \
                x*np.sin(self.rad) + y*np.cos(self.rad) + self.pos.y

        self.plt.plot(x, y + self.ROTATION_OFFSET, color='grey')

        # hexagon
        self.plotLine(-0.5, -1, 2, 3.2)     #  __
        self.plotLine(-1, -0.5, 3.2, 4.4)   # /  \
        self.plotLine(-0.5, 0.5, 4.4, 4.4)  # \  /
        self.plotLine(0.5, 1, 4.4, 3.2)
        self.plotLine(1, 0.5, 3.2, 2)

        # square
        self.plotLine(-1, 1, 2, 2)
        self.plotLine(-1, 1, 1, 1)  #  ____
        self.plotLine(-1, -1, 1, 2) # |____|
        self.plotLine(1, 1, 1, 2)

        # landing legs
        self.plotLine(-1, -1.5, 1.5, 0)
        self.plotLine(1, 1.5, 1.5, 0)   #   /   \
        self.plotLine(-1.3, -1.7, 0, 0) # _/_   _\_
        self.plotLine(1.3, 1.7, 0, 0)

        # engine nozzle
        self.plotLine(-0.2, -0.4, 1, 0)
        self.plotLine(0.2, 0.4, 1, 0)   # /_\
        self.plotLine(-0.4, 0.4, 0, 0)

    ''' Classes and variables to describe the motion of this spaceship (follows SI units) '''

    rad = 0 # anti-clockwise angular displacement of the rocket from the upright position

    class pos():
        x, y = 0, 100

    class vel():
        x, y = 0, 0

    class acc():
        x, y = 0, 0
