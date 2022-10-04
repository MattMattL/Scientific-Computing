'''
Scientific Computing - 1D TISE

Due 15 November 2021

    Description
This program visualises wave functions to helps the user find the ground state of
a given time-independent Schrödinger equation. The user can raise the total energy,
E, until phi(0) reaches zero for the first time, which has the minimum energy and
is the first allowed state (the ground state). The energy slider effectively
simulates the shooting method for each given potential and d(phi)/dx at x=0.1 .

    Features
- Sliders for total energy, potential well width and d(phi)/dx at x = 0.1 .
- Shooting method for finding the ground state.
- Can also find other first few allowed energy levels by keep raising E.
- Plots normalised phi, d(phi)/dx, V and E

    Trivia
- The wave function plotted is normalised
- min(E) = -10 since min(V) = -10
- Phi, V and E are calculated in units of h-bar^2/2ma^

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

''' Function Definitions ''' 

def V(x):
    """ Returns pre-defined potential at x in units of h-bar^2/2ma^2 """
    if x < 0:
    	return INFINITY
    elif x < potentialStepX:
    	return POTENTIAL_LOW
    else:
    	return 0

def reversedV(x):
    """ Returns the reversed potential (starting from x = MAX_X).
        
    This function is used in  since the initial starting point is x = MAX_X but
    updatePhi() propagates from x = 0. (following the equations given in the pdf)
    """
    return V(MAX_X - x)

def phi(x):
    """ Maps x values into the indices of arrPhi and returns arrPhi[index] """
    return arrPhi[int(x / deltaX)]

def phiDeriv(x):
    """ Maps x values into the indices of arrPhiDeriv and returns arrPhiDeriv[index] """
    return arrPhiDeriv[int(x / deltaX)]

def updatePhi():
    """ Updates phi and phi derivative.

    Phi and phi derivative are calculated as if x started from x = 0 and then gets
    flipped before plotting. This is to ensure the halt condition for the shooting
    method is well defined, which, in this case, is phi(x=0) = 0
    """
    global arrPhi, arrPhiDeriv
    global phiPlotData, dPhiPlotData

    arrPhi = [0.01]
    arrPhiDeriv = [initPhiDeriv]

    # update phi and d(phi)/dt from x = 0
    for x in arrX:
        # ignore the element with index number [max length]
        if x == arrX[-1]:
            break

        halfPhi = phi(x) + deltaX/2 * phiDeriv(x)
        halfV = phiDeriv(x) + deltaX/2 * (potentialStepX ** -2) * (reversedV(x) - E) * phi(x)

        arrPhi.append(arrPhi[-1] + deltaX * halfV)
        arrPhiDeriv.append(arrPhiDeriv[-1] + deltaX * (potentialStepX ** -2) * (reversedV(x + deltaX/2) - E) * halfPhi)

    # normalise the wave function
    magnitude = sum([phi*phi*deltaX for phi in arrPhi]) ** 0.5
    arrPhi = [phi/magnitude for phi in arrPhi]

    # reverse the arrays and then plot since the actual starting point is x = MAX_X
    phiPlotData.set_ydata(list(reversed(arrPhi)))
    dPhiPlotData.set_ydata(list(reversed(arrPhiDeriv)))

def updateIndicator():
    """ Updates the y value of the red dot at (x, y) = (0, phi(0)) """
    global indicatorPlotData, phi
    indicatorPlotData.set_ydata(arrPhi[-1])

    # green if falls within the error range. red, otherwise
    if abs(arrPhi[-1]) < TOLERANCE:
        indicatorPlotData.set_color('green')
        indicatorPlotData.set_markersize(12)
    else:
        indicatorPlotData.set_color('red')
        indicatorPlotData.set_markersize(8)

def updatePotential():
    """ Re-draws the 1D potential field """
    global potentialPlotData
    potentialPlotData.set_ydata([V(x) for x in arrX])

def updateEnergyLevel():
    """ Re-draws the bar showing the total energy """
    global energyPlotData, E
    energyPlotData.set_ydata([E, E])

def updatePlot():
    """ Updates all the components in the figure for new E, phi derivative etc. """
    updatePhi()
    updateIndicator()
    updatePotential()
    updateEnergyLevel()

    plt.draw()


''' Callback Functions '''

# declare figure and set figure size
fig = plt.figure(figsize=(0.6*16, 0.6*9))
fig.canvas.manager.set_window_title('Find Your Ground State')

# Slider for adjusting the x value, after which the potential is zero
def stepSliderCallback(val):
    global potentialStepX
    
    potentialStepX = val
    updatePlot()

stepSliderAxes = plt.axes([0.27, 0.05, 0.52, 0.035]) # add new axes to the figure
stepSliderHandler = widgets.Slider(stepSliderAxes, 'Step At:', 0.01, 0.09, valinit=0.05, valfmt='%.3f $m$')
stepSliderHandler.on_changed(stepSliderCallback)

# Slider for adjusting the total energy of the system
def energySliderCallback(val):
    global E
    
    E = val
    updatePlot()

energySliderAxes = plt.axes([0.04, 0.2, 0.03, 0.7]) # add new axes to the figure
energySliderHandler = widgets.Slider(energySliderAxes, r"$E,\frac{\hbar^2}{2ma^2}$J", -10, 10, valinit=-10, valfmt="%4.2f", orientation='vertical')
energySliderHandler.on_changed(energySliderCallback)
energySliderHandler.label.set_size(15)

# Slider for adjusting -d(phi)/dx at x = MAX_X
def derivSliderCallback(val):
    global initPhiDeriv
    
    initPhiDeriv = val
    updatePlot()

derivSliderAxes = plt.axes([0.92, 0.2, 0.03, 0.7]) # add new axes to the figure
derivSliderHandler = widgets.Slider(derivSliderAxes, r"-$\frac{d\phi}{dx}|_{x=0.1}$", -10, 10, valinit=0.1, valfmt="%4.2f", orientation='vertical')
derivSliderHandler.on_changed(derivSliderCallback)
derivSliderHandler.label.set_size(16)


''' Constants '''

INFINITY = 100100100
POTENTIAL_LOW = -10

MAX_X = 0.1
NUM_STEPS = 1000

TOLERANCE = 0.15 # used to check if phi(0) = 0


''' Global Variables '''

E = -10 # total energy of the system
potentialStepX = 0.05 # V = 0 for all x > potentialStepX
initPhiDeriv = 0.1 # initial value of d(phi)/dx at x = MAX_X

arrPhi = [] # phi values
arrPhiDeriv = [] # d(phi)/dx values

arrX = np.linspace(0, MAX_X, NUM_STEPS)
deltaX = arrX[1]


''' Code '''

# set plot axes size and axis labels
plotAxes = plt.axes([0.18, 0.2, 0.7, 0.7])

plotAxes.set_title(r"Increase E from $-10(\hbar^2/2ma^2)$ $(J)$ until $\phi(0)$ first reaches zero", fontsize=13)
plotAxes.set_xlabel(r"$x, m$").set_size(14)
plotAxes.set_ylabel(r"$E,\frac{\hbar^2}{2ma^2}$ J").set_size(14)

# plot the potential
arrPotential = [V(x) for x in arrX]
potentialPlotData, = plotAxes.plot(arrX, arrPotential, color='black', linewidth=2)

# the potential barrier at x = 0
plotAxes.plot([0, 0], [-10, 11], color='black', linewidth=2)

# plot dummy graphs and save the returned object to update the y values later
dummyZeros = np.empty(NUM_STEPS)
dummyZeros.fill(0)

phiPlotData, = plotAxes.plot(arrX, dummyZeros, color='red')
dPhiPlotData, = plotAxes.plot(arrX, dummyZeros, color='grey', linestyle='--', linewidth=0.5)

# plot a black indicator at (x, y) = (0, 0)
plotAxes.plot(0, 0, color='black', marker='.', markersize=6)

# plot a red indicator at (x, y) = (0, phi(0))
indicatorPlotData, = plotAxes.plot(0, 0, color='red', marker='.', markersize=8)

# plot the total energy of the system
energyPlotData, = plotAxes.plot([0, MAX_X], [E, E], color='black', linestyle='--', linewidth=0.5)

# set axis limits
plotAxes.set_xlim(-0.005, MAX_X+0.005)
plotAxes.set_ylim(-11, 11)

# add legends
phiPlotData.set_label(r"$\phi(x), Normalised$")
dPhiPlotData.set_label(r"$d\phi/dx$")
potentialPlotData.set_label("Potential")
energyPlotData.set_label("Total E")

plotAxes.legend()

# run initial update and display
updatePlot()
plt.show()