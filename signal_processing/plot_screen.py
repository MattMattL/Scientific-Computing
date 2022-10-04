import numpy as np
import matplotlib.pyplot as plt

from fourier import *

class PlotScreen:

    # basic settings for the initial plots
    maxTime = 3 # second
    numPoints = 200 # the number of plotting points
    frequency = 1 # 1/second

    # arrays for saving x, masked y and unmasked y values
    arrTime = np.linspace(0, maxTime, numPoints)
    arrWave = sinf(arrTime, frequency)
    arrMaskedWave = sinf(arrTime, frequency)

    # the percentage of each plot to be masked (from left and from right)
    leftPhaseMaskPercent, rightPhaseMaskPercent = 0, 100
    leftFreqMaskPercent, rightFreqMaskPercent = 0, 100

    # two windowing bars. they are saved so it can be deleted later
    leftMaskPlot, rightMaskPlot = None, None

    # plot title for each graph
    annotation1, annotation2 = None, None

    # variables used when generating a new wave (to be added to the existing wave)
    arrNewWave = None
    newFrequencyPercent = 10 # 100% means the Nyquist frequency, 0% means a constant line
    newAmplitudeModifier = 0.25
    newOffsetPercent = 0 # phase offset in percentage. goes from -50% to 50% of the current wavelength

    # horizontal and vertical magnifier for the phase and k-space plots
    horPhaseScaler, verPhaseScaler = 1, 1
    horFreqScaler, verFreqScaler = 1, 1

    def __init__(self, interfaceIn, plt):
        # save frequently used objects locally
        self.interface = interfaceIn
        self.plt = plt

        # two plot axes for each "screen"
        self.axes1 = self.plt.axes([0.05, 0.47, 0.4, 0.4], facecolor=[0, 0, 0])
        self.axes2 = self.plt.axes([0.05, 0.07, 0.4, 0.4], facecolor=[0, 0, 0])

        # initialise x and y limits suitable for the initial wave
        self.axes1.set_xlim([0, self.maxTime])
        self.axes1.set_ylim([-2, 2])
        self.axes2.set_xlim([0, self.maxTime])
        self.axes2.set_ylim([-2, 2])

        # plot the initial sin wave (like a showcase)
        self.plotHandler1, = self.axes1.plot(self.arrTime, self.arrWave, color='white')
        self.plotHandler2, = self.axes2.plot(self.arrTime, self.arrMaskedWave, color='yellow')
        
        # set and save plot titles. saving the return values allows the text to be changed later
        self.annotation1 = self.axes1.annotate("Default Sin Wave (amp vs time/s)", xy=(0.04, 0.9), xycoords='axes fraction', color='white')
        self.annotation2 = self.axes2.annotate("Reconstructed with FT", xy=(0.04, 0.9), xycoords='axes fraction', color='white')

        # set the grid and hide labels for the appearance
        self.axes1.grid(linestyle='--', linewidth=0.2, color='green')
        self.axes2.grid(linestyle='--', linewidth=0.2, color='green')
        self.axes1.set_xticklabels([])

        # initialise arrNewWave for the Adder function
        self.arrNewWave = np.empty(self.numPoints)
        self.arrNewWave.fill(0)

    # returns the Nyquist frequency for the current setting
    def getNyquistFreq(self):
        return self.numPoints / self.maxTime / 2

    
    def updateX(self, id, arrX):
        """
        Update the x values of one of the two plot screens.

        Parameters:
            id: 1 is to update the first screen (above), 2 is to update the second screen (below)
            arrX: array of new x values
        """

        if id == 1:
            self.plotHandler1.set_xdata(arrX)
        elif id == 2:
            self.plotHandler2.set_xdata(arrX)

    def updateY(self, id, arrY):
        """
        Update the y values of one of the two plot screens.

        Parameters:
            id: 1 is to update the first screen (above), 2 is to update the second screen (below)
            arrY: array of new y values
        """

        if id == 1:
            self.plotHandler1.set_ydata(arrY)
        elif id == 2:
            self.plotHandler2.set_ydata(arrY)

    # returns the masked (= set to 0) array of the original wave
    def getMaskedWave(self):
        arr = []
        # calculate the indices to be masked from the set percentages and numPoints
        leftLimitIndex = self.leftPhaseMaskPercent/100 * self.numPoints
        rightLimitIndex = self.numPoints - (1 - self.rightPhaseMaskPercent/100)*self.numPoints

        # set values outside the windowing limits to zero
        for i in range(self.numPoints):
            if leftLimitIndex <= i <= rightLimitIndex:
                arr.append(self.arrWave[i])
            else:
                arr.append(0)

        return arr

    # returns the masked Fourier transform of the original wave
    def getMaskedFourier(self):
        # perform Fourier transformation
        fourier, kSpace = fourier_transform(self.getMaskedWave(), self.maxTime)

        arr = []
        # calculate the indices to be masked from the set percentages and numPoints
        leftLimitIndex = self.leftFreqMaskPercent/100 * self.numPoints
        rightLimitIndex = self.numPoints - (1 - self.rightFreqMaskPercent/100)*self.numPoints

        # set values outside the windowing limits to zero
        for i in range(self.numPoints): 
            if leftLimitIndex <= i <= rightLimitIndex:
                arr.append(fourier[i])
            else:
                arr.append(0)

        return arr, kSpace

    # deletes the previous title and re-draws a new one at the right location
    def updateAnnotation(self, id, text, posX=0.04):
        if id == 1:
            self.annotation1.remove()
            self.annotation1 = self.axes1.annotate(text, xy=(posX, 0.9), xycoords='axes fraction', color='white')
        elif id == 2:
            self.annotation2.remove()
            self.annotation2 = self.axes2.annotate(text, xy=(posX, 0.9), xycoords='axes fraction', color='white')

    def updatePlot(self):
        # 1) plot the original wave with no windowing applied
        # 2) plot the reconstructed wave by FT -> IFT (with phase and k-space windowing)
        if self.interface.mode == self.interface.Mode.PHASE:
            # plot the original wave with windowing limits
            maskedWave = []
            leftLimitIndex = self.leftPhaseMaskPercent/100 * self.numPoints
            rightLimitIndex = self.numPoints - (1 - self.rightPhaseMaskPercent/100)*self.numPoints - 1

            # apply windowing to the original wave
            for i in range(self.numPoints):
                if leftLimitIndex <= i <= rightLimitIndex:
                    maskedWave.append(self.arrWave[i])
                else:
                    maskedWave.append(0)

            self.updateX(1, self.arrTime)
            self.updateY(1, maskedWave)

            # plot the Fourier version of the wave
            arrFourierOfMaskedWave, kSpace = self.getMaskedFourier()
            inverse_fourier, tSpace = inverse_fourier_transform(arrFourierOfMaskedWave, kSpace[-1])
            
            self.updateX(2, self.arrTime)
            self.updateY(2, inverse_fourier)

            # plot two windowing indicators
            iLeft = max(0, min(self.numPoints-1, int(leftLimitIndex)))
            iRight = max(0, min(self.numPoints-1, int(rightLimitIndex)))
            minY, maxY = min(self.arrWave)-10, max(self.arrWave)+10

            # delete previous windowing-limit plots to draw new ones
            if self.leftMaskPlot is not None: self.axes1.lines.remove(self.leftMaskPlot)
            if self.rightMaskPlot is not None: self.axes1.lines.remove(self.rightMaskPlot)

            # visualise the left, right windowing limits and save it to delete later
            self.leftMaskPlot = self.axes1.plot([self.arrTime[iLeft], self.arrTime[iLeft]], [minY, maxY], linestyle='--', linewidth=0.7, color='blue')[0]
            self.rightMaskPlot = self.axes1.plot([self.arrTime[iRight], self.arrTime[iRight]], [minY, maxY], linestyle='--', linewidth=0.5, color='white')[0]

            # set axis limits according to the current wave size and the magnifier settings
            limY = 2 * max(abs(min(self.arrWave)), max(self.arrWave))

            self.axes1.set_xlim([0, self.maxTime / self.horPhaseScaler])
            self.axes1.set_ylim([-max(0.1, limY / self.verPhaseScaler), max(0.1, limY / self.verPhaseScaler)])
            self.axes2.set_xlim([0, self.maxTime / self.horPhaseScaler])
            self.axes2.set_ylim([-max(0.1, limY / self.verPhaseScaler), max(0.1, limY / self.verPhaseScaler)])

            # add plot description as annotations
            self.updateAnnotation(1, "Original Wave (amp vs time/s)")
            self.updateAnnotation(2, "Reconstructed with FT")

            # update knob positions
            self.interface.windowingKnobs.updateLeftKnob(self.leftPhaseMaskPercent)
            self.interface.windowingKnobs.updateRightKnob(self.rightPhaseMaskPercent)
            self.interface.scalerKnobs.updateHorizontalKnob(self.horPhaseScaler)
            self.interface.scalerKnobs.updateVerticalKnob(self.verPhaseScaler)

        # 1) plot the k-space of the original wave with windowing
        # and 2) without windowing
        elif self.interface.mode == self.interface.Mode.FREQUENCY:
            # plot amplitude vs k-space for the original wave
            fourierOfMaskedWave, kSpace = fourier_transform(self.getMaskedWave(), self.maxTime)

            fourierAmplitude = [x*x.conjugate()/self.numPoints for x in fourierOfMaskedWave]
            self.updateX(1, kSpace)
            self.updateY(1, fourierAmplitude)

            # plot amplitude vs k-space for the original wave (windowing in k-space applied)
            maskedFourier = []
            leftLimitIndex = self.leftFreqMaskPercent/100 * self.numPoints
            rightLimitIndex = self.numPoints - (1 - self.rightFreqMaskPercent/100)*self.numPoints

            # apply windowing to the Fourier transform
            for i in range(self.numPoints): 
                if leftLimitIndex <= i <= rightLimitIndex:
                    maskedFourier.append(fourierOfMaskedWave[i])
                else:
                    maskedFourier.append(0)

            self.updateX(2, kSpace)
            self.updateY(2, [x*x.conjugate()/self.numPoints for x in maskedFourier])

            # plot two windowing indicators
            iLeft = max(0, int(leftLimitIndex))
            iRight = min(len(kSpace)-1, int(rightLimitIndex))
            minY, maxY = min(fourierAmplitude)-10, max(fourierAmplitude)+10

            # delete previous windowing-limit plots to draw new ones
            if self.leftMaskPlot is not None: self.axes1.lines.remove(self.leftMaskPlot)
            if self.rightMaskPlot is not None: self.axes1.lines.remove(self.rightMaskPlot)

            # visualise the left, right windowing limits and save it to delete later
            self.leftMaskPlot = self.axes1.plot([kSpace[iLeft], kSpace[iLeft]], [minY, maxY], linestyle='--', linewidth=0.7, color='blue')[0]
            self.rightMaskPlot = self.axes1.plot([kSpace[iRight], kSpace[iRight]], [minY, maxY], linestyle='--', linewidth=0.5, color='white')[0]

            # set axis limits according to the current wave size and the magnifier settings
            self.axes1.set_xlim([-1, (kSpace[-1]+1) / self.horFreqScaler])
            self.axes1.set_ylim([-1, (max(fourierAmplitude)+5) / self.verFreqScaler])
            self.axes2.set_xlim([-1, (kSpace[-1]+1) / self.horFreqScaler])
            self.axes2.set_ylim([-1, (max(fourierAmplitude)+5) / self.verFreqScaler])

            # update annotations to explain what the plots are showing
            self.updateAnnotation(1, "K-Space of the Original Wave (amp vs f/$s^-1$)")
            self.updateAnnotation(2, "Masked K-Space")

            # update the knob positions
            self.interface.windowingKnobs.updateLeftKnob(self.leftFreqMaskPercent)
            self.interface.windowingKnobs.updateRightKnob(self.rightFreqMaskPercent)
            self.interface.scalerKnobs.updateHorizontalKnob(self.horFreqScaler)
            self.interface.scalerKnobs.updateVerticalKnob(self.verFreqScaler)

        # 1) plot the preview of 'the current wave + newly generated wave'
        # 2) plot the newly generated wave
        elif self.interface.mode == self.interface.Mode.ADD_NEW:
            # calculate the frequency in range [0.001, Nyquist] of a new sin/cos wave.
            frequency = self.newFrequencyPercent/100 * self.getNyquistFreq()
            
            # calculate phase with phase shift (from the user input) taken into account
            phaseWithShift = 2 * np.pi * frequency * (self.arrTime - self.newOffsetPercent/100/frequency)

            # calculate the final wave (multiplied by amplitude from the user input)
            self.arrNewWave = self.newAmplitudeModifier * np.sin(phaseWithShift)

            # update x, y values
            self.updateX(1, self.arrTime)
            self.updateY(1, self.arrWave + self.arrNewWave)
            self.updateX(2, self.arrTime)
            self.updateY(2, self.arrNewWave)

            # update annotations to explain what the plots are showing
            self.updateAnnotation(1, "Current Wave + New Wave (preview) (amp vs time/$s$)")
            self.updateAnnotation(2, "New Wave (press Confirm to add)")

            # update x, y limits according to the current and new wave size
            limY = 2 * max(abs(min(self.arrWave)), max(self.arrWave))

            self.axes1.set_xlim([0, self.maxTime])
            self.axes1.set_ylim([-max(2, limY), max(2, limY)])
            self.axes2.set_xlim([0, self.maxTime])
            self.axes2.set_ylim([-max(2, limY), max(2, limY)])

        # update the information panel showing # of points and Nyquist frequency
        self.interface.informationPanel.updateNumPoints()
        self.interface.informationPanel.updateNyquist()

        # draw to show the updated plots and graphics
        self.plt.draw()
