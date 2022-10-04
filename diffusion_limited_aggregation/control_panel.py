import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.adder_control import AdderControl
from components.preset_control import PresetControl
from components.seeder_control import SeederControl
from components.colour_palette_control import ColourPaletteControl
from components.random_seed_control import RandomSeedControl

from components.mode_control import ModeControl
from components.info_analysis import InfoAnalysis
from components.best_fit_analysis import BestFitAnalysis
from components.save_analysis import SaveAnalysis

class ControlPanel:

    def __init__(self, program, plt):
        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # initialise control and analysis axes and their properties
        self.controlAxes = self.plt.axes([0, 0, 0.25, 1], facecolor=(0.25, 0.25, 0.25))
        self.analysisAxes = self.plt.axes([0.75, 0, 0.25, 1], facecolor=(0.25, 0.25, 0.25))

        self.controlAxes.xaxis.set_visible(False)
        self.controlAxes.yaxis.set_visible(False)

        self.analysisAxes.xaxis.set_visible(False)
        self.analysisAxes.yaxis.set_visible(False)

        # initialise control panel components
        self.presetControl = PresetControl(self.program, self.plt)
        self.adderControl = AdderControl(self.program, self.plt)
        self.seederControl = SeederControl(self.program, self.plt)
        self.colourPaletteControl = ColourPaletteControl(self.program, self.plt)
        self.randomSeedControl = RandomSeedControl(self.program, self.plt)
        self.modeButtons = ModeControl(self.program, self.plt)

        # initialise analysis panel components
        self.infoAnalysis = InfoAnalysis(self.program, self.plt)
        self.bestFitAnalysis = BestFitAnalysis(self.program, self.plt)
        self.saveAnalysis = SaveAnalysis(self.program, self.plt)


        ''' Component Ideas

        x buttons: set lattice size (implemented and then removed)
        o sliders: change relative bias for random direction
        - sliders: adjust sticking probability

        o buttons: set seeds

        o sliders: starting & tending colour

        x sliders: zoom in & out
        x buttons: move screen around

        o buttons: add more points
        o sliders: change # of points to add per button press

        x sliders: adjust plot scale
        o buttons: save plot

        '''


