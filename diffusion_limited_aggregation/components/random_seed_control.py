import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class RandomSeedControl(ComponentBase, object):

    x = 0.005
    y = 0.21

    def setSeedCallback(self, text):
        """ Takes a string and sets the random seed number """
        if text == "":
            newSeed = 0
        else:
            newSeed = int(text)

        self.program.lattice.setRandomSeed(newSeed)
        self.annHandle.set(text="Current Seed = {0:d}".format(newSeed))

    def __init__(self, program, plt):
        # initialise the parent class
        super(RandomSeedControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        ''' Initialise Group Panel '''

        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.16])
        self.addGroupTitle(self.groupAxes, "4. Random Seed Setting", (0.02, 0.8))

        ''' Text Box and Annotations ''' 

        # annotation showing the current seed
        seed = self.program.lattice.getRandomSeed()

        self.annHandle = self.addAnnotation("Current Seed = {0:d}".format(seed), (0.06, 0.5))

        # text box
        pos = [self.x+0.11, self.y+0.02, 0.08, 0.04]
        self.seedTextHandle = self.addTextBox(pos, "Set New Seed: ", str(seed), self.setSeedCallback)