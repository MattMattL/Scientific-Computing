import numpy as np
import matplotlib.pyplot as plt
import random

from lattice import Lattice
from plot_screen import PlotScreen
from control_panel import ControlPanel
from analysis_screen import AnalysisScreen

class DLASimulator:
    """
    The main class containing the basic components of the DLA simulator. To see
    individual components for control and analysis panels, see class::ControlPanel.
    """

    UID = None

    def __init__(self):
        # get a unique id for this run
        self.UID = random.randint(0, 10000)

        # initialise figure and set screen size & ratio
        self.fig = plt.figure(figsize=(0.7*16, 0.7*9))
        self.fig.canvas.manager.set_window_title("Simulator")

        # initialise program components
        self.initialise()

        plt.show()

    def initialise(self):
        self.lattice = Lattice(self, plt, 11, 11)
        self.plotScreen = PlotScreen(self, plt)
        self.analysisScreen = AnalysisScreen(self, plt)
        self.controlPanel = ControlPanel(self, plt)

def main():
    program = DLASimulator()

if __name__ == "__main__":
    main()
