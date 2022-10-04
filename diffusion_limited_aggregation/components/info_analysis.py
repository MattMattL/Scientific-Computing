import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from math import log10, floor

from components.component_base import ComponentBase

class InfoAnalysis(ComponentBase, object):

    x = 0.755
    y = 0.69

    ''' Functions for updating the information panel '''

    def updatePlotDescription(self, description):
        self.descriptionHandle.set(text="Plot: " + description)

    def updateCount(self, count):
        self.countHandle.set(text="Number of Particles = " + "{0:d}".format(count))

    def updateY(self, y):
        self.yHandle.set(text="y = " + "{0:.2f}".format(y))

    def updateSlope(self, slope):
        self.slopeHandle.set(text="dy/dx = " + "{0:.2f}".format(slope))

    def updateError(self, error):
        # Rounding a number to its first significant figure by Egveny on StackOverflow (last checked 16 Dec 2021)
        # https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
        # oneSignificantPlace = round(error, -int(floor(log10(abs(error)))))
        self.errorHandle.set(text="Std Err of Slope = " + "{0:.6f}".format(error) + " ({0:.1g})".format(error))


    def __init__(self, program, plt):
        # initialise the parent class
        super(InfoAnalysis, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        ''' Group Panel and Annotations '''

        # initialise group panel and set the title
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.3])
        self.addGroupTitle(self.groupAxes, "6.1. Data", (0.03, 0.86))

        ''' Add information on the panel '''

        # show plot axis description
        self.descriptionHandle = self.addAnnotation("Plot: ", (0.03, 0.62))

        # show the number of particles
        self.countHandle = self.addAnnotation("Number of Particles = ", (0.03, 0.5))

        # show y value
        self.yHandle = self.addAnnotation("y = ", (0.03, 0.35))
        
        # show dy/dx
        self.slopeHandle = self.addAnnotation("dy/dx = ", (0.03, 0.2))

        # mean squared error in the windowing limits
        self.errorHandle = self.addAnnotation("Std Err of Slope", (0.03, 0.05))

        # initialise panel
        self.updatePlotDescription("$-y$ versus $x$\n")
        self.updateY(3)
        self.updateSlope(1.6)
