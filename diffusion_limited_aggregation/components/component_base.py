import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class ComponentBase:
    """ The parent class for all panel classes. Makes it easy to put sliders, buttons, etc. """

    PANEL_COLOUR = [0.2, 0.2, 0.2]
    TEXT_COLOUR = [0.9, 0.9, 0.9]
    SLIDER_FOREGROUND = [0.6, 0.3, 0.8]
    SLIDER_BACKGROUND = [0.15, 0.15, 0.15]

    def __init__(self, program, plt):
        self.program = program
        self.plt = plt

    def addGroupPanel(self, pos):
        """ Adds and initialises axes representing a grouop panel """

        axes = self.plt.axes(pos, facecolor=self.PANEL_COLOUR)

        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)

        return axes

    def addGroupTitle(self, groupAxes, text, pos):
        """ Adds a group title as an annotation """
        groupAxes.annotate(text, xy=pos, xycoords='axes fraction', color=self.TEXT_COLOUR)

    def addButton(self, pos, text, callback):
        """ Adds a button at a given position and returns the axes and handler """

        axes = self.plt.axes(pos)
        handler = widgets.Button(axes, text)
        handler.on_clicked(callback)

        return axes, handler

    def addSlider(self, pos, label, min, max, initial, format, callback):
        """ Adds a slider and returns the handler """

        axes = self.plt.axes(pos, facecolor=self.SLIDER_BACKGROUND)
        handler = widgets.Slider(axes, label, min, max, valinit=initial, valfmt=format, color=self.SLIDER_FOREGROUND)
        handler.on_changed(callback)

        handler.label.set_color(self.TEXT_COLOUR)
        handler.valtext.set_color(self.TEXT_COLOUR)

        return axes, handler

    def addAnnotation(self, text, pos):
        """ Adds an annotation and returns the result object """
        return self.groupAxes.annotate(text, xy=pos, xycoords='axes fraction', color=self.TEXT_COLOUR)

    def addTextBox(self, pos, label, initial, callback):
        """ Adds a text box and returns the handler """

        axes = self.plt.axes(pos)
        handler = widgets.TextBox(axes, label, initial=initial)
        handler.on_submit(callback)

        handler.label.set_color(self.TEXT_COLOUR)

        return handler
