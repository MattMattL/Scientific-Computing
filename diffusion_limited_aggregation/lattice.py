import numpy as np
import matplotlib.pyplot as plt
import math
import random

class Lattice:
    """
    This class takes all position information in terms of x and y coordinates,
    and the values are converted into row and column to be used internally.
    Other classes use x and y, only this class processes in terms of row and column.
    """

    ''' Uninitialised Variables

    ROW, COL, map

    '''

    MAP_SIZE = 1000
    INT_HALF_MAP_SIZE = int(MAP_SIZE / 2)
    EXTRA_RADIUS = 5

    particleCount = 0 # the number of particles excluding the seeds
    maxRadius = 1
    
    bias = [1, 1, 1, 1] # bias used to choose a random direction
    cumulativeBias = [1, 2, 3, 4] # cumulative bias for each direction: Right, Up, Left, Down

    randomSeed = 1234

    def __init__(self, program, plt, row, col):
        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # initialising a 2D array in one line (last checked 16 Nov 2021):
        # https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        self.map = [[False] * self.MAP_SIZE for i in range(self.MAP_SIZE)]

        # set random seed, 1234 for testing
        np.random.seed(self.randomSeed)

        # set an initial seed at the centre
        self.set(0, 0, True)

    def _isInBoundary(self, row, col):
        """ Returns True iff a given position is in the map (not out of boundary). """
        return (0 <= row < self.MAP_SIZE) and (0 <= col < self.MAP_SIZE)

    def _hasNeighbour(self, row, col):
        """ Returns True iff there is at least one adjacent particle around. """

        return self.get(row+1, col) or \
                self.get(row-1, col) or \
                self.get(row, col+1) or \
                self.get(row, col-1)

    def _getRowColfromXY(self, x, y):
        return int(y + self.INT_HALF_MAP_SIZE), int(x + self.INT_HALF_MAP_SIZE)

    def _getXYfromRowCol(self, row, col):
        return col - self.INT_HALF_MAP_SIZE, row - self.INT_HALF_MAP_SIZE


    def get(self, row, col):
        """ Returns the boolean value at a given position if it is in the boundary """
        return self.map[row][col] if self._isInBoundary(row, col) else False


    def set(self, x, y, value):
        """ Sets the value at a given position.

        Parameters
            value: True or False
        """

        row, col = self._getRowColfromXY(x, y)

        if self._isInBoundary(row, col):
            self.map[row][col] = value
        else:
            print("[Error] <Lattice::set> Out of boundary: {}, {}".format(row, col))

    def setBias(self, value, direction):
        """ Sets bias of a direction and re-calculates the cumulative distribution """

        # update the bias array
        if direction == "RIGHT": self.bias[0] = value
        elif direction == "UP": self.bias[1] = value
        elif direction == "LEFT": self.bias[2] = value
        elif direction == "DOWN": self.bias[3] = value
        else: print("[Error] <Lattice:setBias> Undefined Condition")

        # update the cumulative bias (Right -> Up -> Left -> Down)
        self.cumulativeBias = [sum(self.bias[j] for j in range(i+1)) for i in range(0, 4)]

    def setRandomSeed(self, seed):
        self.randomSeed = seed
        np.random.seed(self.randomSeed)

    def getRandomSeed(self):
        return self.randomSeed

    def reset(self):
        """ Resets the map and fills with False. """
        self.map = [[False] * self.MAP_SIZE for i in range(self.MAP_SIZE)]

    def add(self):
        """ Adds a new particle on the map by choosing a random direction, with bias. """

        # choose a random location on a circle to place the particle
        r = self.maxRadius + self.EXTRA_RADIUS
        theta = np.random.uniform(0, 2*np.pi)

        newRow = int(self.INT_HALF_MAP_SIZE + r*np.cos(theta))
        newCol = int(self.INT_HALF_MAP_SIZE + r*np.sin(theta))

        # pre-calculate frequently used constants to boost up the speed
        BOUNDARY_OFFSET = self.INT_HALF_MAP_SIZE - r
        TWO_TIMES_R = r << 1
        MAX_BOUNDARY, MIN_BOUNDARY = self.INT_HALF_MAP_SIZE + r, self.INT_HALF_MAP_SIZE - r

        # randomly translate the particle until it touches another particle
        while not self._hasNeighbour(newRow, newCol):
            # choose a random direction
            direction = np.random.uniform(0, self.cumulativeBias[-1])

            # translate to the direction
            if direction < self.cumulativeBias[0]: newCol += 1
            elif direction < self.cumulativeBias[1]: newRow -= 1
            elif direction < self.cumulativeBias[2]: newCol -= 1
            else: newRow += 1

            # check if the particle is outside the boundary
            # (the boundary changes dynamically for better performance)
            if not (MIN_BOUNDARY < newRow < MAX_BOUNDARY) or not (MIN_BOUNDARY < newCol < MAX_BOUNDARY):
                # translate to (x, y) coordinate (centred around (0, 0))
                newRow = newRow - BOUNDARY_OFFSET
                newCol = newCol - BOUNDARY_OFFSET

                # get modulus to keep it inside the boundary
                newRow %= TWO_TIMES_R
                newCol %= TWO_TIMES_R

                # back to (row, col) coordinate
                newRow = newRow + BOUNDARY_OFFSET
                newCol = newCol + BOUNDARY_OFFSET

        # new allowed position found, register the particle
        if self._isInBoundary(newRow, newCol):
            self.map[newRow][newCol] = True
            self.particleCount += 1

            self.program.controlPanel.infoAnalysis.updateCount(self.particleCount)

            # update max radius for next function call
            x, y = self._getXYfromRowCol(newRow, newCol)

            newRadius = int(math.sqrt(x*x + y*y))
            self.program.analysisScreen.registerRadius(newRadius)

            if newRadius > self.maxRadius:
                self.maxRadius = newRadius

            # return the new coordinate for external uses
            return x, y

        else:
            print("[Error] <Lattice::add> Out of boundary")
            return None, None


