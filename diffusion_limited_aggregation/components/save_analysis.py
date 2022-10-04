import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class SaveAnalysis(ComponentBase, object):

    SERIAL_NUMBER = None
    mapFigCount = 0
    plotFigCount = 0

    x = 0.755
    y = 0.01

    def saveXYCallback(self, event):
        """ Takes a screenshot of the x-y plot and saves as a file """

        # frequently called objects
        fig = self.program.fig
        axes = self.program.plotScreen.axes
        numParticles = self.program.lattice.particleCount
        
        # adjust the position and update the title
        self.program.plotScreen.showScreen()
        self.program.analysisScreen.hideScreen()

        oldPosition = axes.get_position()
        axes.set_position([0.32, 0.1, 0.36, 0.55])
        
        axes.set_xlabel("x", fontsize=13)
        axes.set_ylabel("y", fontsize=13)

        # How to crop a figure by Joe Kington (last checked 27 Nov 2021):
        # https://stackoverflow.com/questions/4325733/save-a-subplot-in-matplotlib?rq=1
        extent = axes.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        
        self.mapFigCount += 1
        filename = "map_" + "{0:04d}".format(self.program.UID) + "_{0:02d}".format(self.mapFigCount) + ".png"
        fig.savefig("./figures/" + filename, bbox_inches=extent.expanded(1.36, 1.3))

        # post-initialisation
        axes.set_position(oldPosition)

        self.annotHandle.set(text=filename)
        self.plt.pause(0.001)

    def saveLogLogCallback(self, event):
        """ Takes a screenshot of the log-log plot and saves as a file """

        # frequently called objects
        fig = self.program.fig
        axes = self.program.analysisScreen.axes
        
        # adjust the position and update the title
        self.program.plotScreen.hideScreen()
        self.program.analysisScreen.showScreen()
        
        oldPosition = axes.get_position()
        axes.set_position([0.32, 0.1, 0.36, 0.55])

        axes.set_xlabel("log of radius, log(R)", fontsize=11, labelpad=10)
        axes.set_ylabel("log of the number of particles within radius R", fontsize=11, labelpad=10)

        axes.legend()

        # How to crop a figure by Joe Kington (last checked 27 Nov 2021):
        # https://stackoverflow.com/questions/4325733/save-a-subplot-in-matplotlib?rq=1
        extent = axes.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        
        self.plotFigCount += 1
        filename = "plot_" + "{0:04d}".format(self.program.UID) + "_{0:02d}".format(self.plotFigCount) + ".png"
        fig.savefig("./figures/" + filename, bbox_inches=extent.expanded(1.35, 1.35))

        # post-initialisation
        axes.set_xlabel("")
        axes.set_ylabel("")

        axes.set_position(oldPosition)
        axes.get_legend().remove()

        self.annotHandle.set(text=filename)
        self.plt.pause(0.001)

    def __init__(self, program, plt):
        # initialise the parent class
        super(SaveAnalysis, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        ''' Group Panel '''

        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.15])
        self.addGroupTitle(self.groupAxes, "7. Save Figures", (0.03, 0.8))

        ''' Buttons and Annotations '''

        # buttons for saving the x-y axes and the plot axes
        buttonX, buttonY = 0.1, 0.05

        pos = [self.x+0.01, self.y+0.01, buttonX, buttonY]
        self.saveXYSpaceHandle = self.addButton(pos, "X-Y Space", self.saveXYCallback)

        pos = [self.x+buttonX+0.03, self.y+0.01, buttonX, buttonY]
        self.saveLogLogHandle = self.addButton(pos, "Log-Log Space", self.saveLogLogCallback)

        # annotation showing if the plot was saved
        self.annotHandle = self.addAnnotation("", (0.03, 0.55))
