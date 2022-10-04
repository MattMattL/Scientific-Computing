'''
Module      Scientific Computing
Project     Lunar Lander

Started     5 October 2021
Deadline    18 October 2021

    Description
This game simulates the physics of a lunar lander landing on the surface of the
moon (with g = 1 m/s^2, towards the surface) using Newton's equation of motion.

    Program Extensions
- Keyboard and slider control
- Variable angle of the lunar lander
- Randomised terrain
- Better graphics
- Speedometer-style control panel
- Fuel limit

    Files
- LunarLander.py
- map.py
- spaceship.py
- control_panel.py
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import time

from map import Map
from spaceship import Spaceship
from control_panel import ControlPanel


''' Function Definitions '''

# returns True if the lander is on the ground
def isLanderOnGround():
    return lander.pos.y <= landscape.getElevationAt(lander.pos.x)

# key press callback from the official documentation (last checked 9 Oct 2021):
# https://matplotlib.org/3.2.1/gallery/event_handling/keypress_demo.html
def rotationKeyPressed(event):
    global lander

    if event.key == 'a':
        lander.rad += np.pi / 6
    elif event.key == 'd':
        lander.rad -= np.pi / 6

    lander.fuel -= 0.5

fig, keyInputAxes = plt.subplots(1, facecolor=(0.08, 0.08, 0.08))
fig.canvas.mpl_connect('key_press_event', rotationKeyPressed)
fig.canvas.set_window_title('Lunar Lander')
keyInputAxes.axis("off")

# event handler for a slider by James Clewett, copied from Moodle (last checked 12 Oct 2021):
# https://moodle.nottingham.ac.uk/pluginfile.php/8082332/mod_resource/content/2/widgetsdemo.py
def mainEngineSlider(val):
    global mainEngineThrust
    mainEngineThrust = val

sliderAxes = plt.axes([0.85, 0.2, 0.05, 0.7], facecolor=(40/256, 41/256, 35/256))
sliderWidget = widgets.Slider(sliderAxes, 'Engine Setting', 0, 3,
        valinit=0, valfmt='%.2f $m/s^2$', orientation='vertical', color=(0.8, 0.3, 0.2))
sliderWidget.label.set_color('white')
sliderWidget.valtext.set_color('white')
sliderWidget.on_changed(mainEngineSlider)


''' Global Variables '''

MOON_GRAVITY = -1 # acceleration due to gravity on the moon. +a is in the +y direction

# set main screen and control panel size
plotAxes = plt.axes([0.1, 0.2, 0.7, 0.7], facecolor=(40/256, 41/256, 35/256))
panelAxes = plt.axes([0.1, 0.05, 0.84, 0.12])

# set initial thrust to 0
mainEngineThrust = 0
sideEngineThrust = 0

deltaTime = 0 # time elapsed since last frame
totalTime = 0 # time elapsed since first frame

# initialise classes
landscape = Map(plotAxes)
lander = Spaceship(plotAxes)
controlPanel = ControlPanel(panelAxes, landscape, lander)


''' Code '''

# turn off numeric annotations for the main screen axes
plotAxes.xaxis.set_visible(False)
plotAxes.yaxis.set_visible(False)

# generate and print frames until the game ends
while not isLanderOnGround():
    # update variables
    startTime = time.time()

    mainEngineThrust = min(lander.fuel, mainEngineThrust)

    lander.acc.x = -mainEngineThrust * np.sin(lander.rad) # Newton's equation of motion
    lander.acc.y = MOON_GRAVITY + mainEngineThrust * (np.cos(lander.rad))
    lander.fuel -= max(mainEngineThrust * deltaTime, 0)

    screenHeight = lander.pos.y + 20
    screenWidth = screenHeight

    # generate the next frame
    plotAxes.clear()
    panelAxes.clear()
    
    lander.tick(deltaTime) # updates position and velocity

    landscape.plot(screenWidth, lander.pos.x) # updates graphics
    lander.plot(mainEngineThrust)
    controlPanel.plot()

    plotAxes.set_title("only 1% can beat this game\n(press A/D to activate the side engines)", color='white') # reset title
    panelAxes.axis("off")

    formatted = "time taken = {0:.3f} $s$".format(totalTime)
    plotAxes.annotate(formatted, xy=(0.01, 0.95), xycoords='axes fraction', color='white') # reset time annotation

    # draw the new frame
    plotAxes.set_xlim(lander.pos.x - screenWidth/2, lander.pos.x + screenWidth/2)
    plotAxes.set_ylim(-10, screenHeight - 10)

    panelAxes.set_xlim(0, 15.4)
    panelAxes.set_ylim(-1, 1.1)

    plt.pause(0.001)
    plt.draw()

    # prepare for the next iteration
    deltaTime = time.time() - startTime
    
    if not isLanderOnGround(): # ignore deltaTime from the last frame (due to update order)
        totalTime += deltaTime

plotAxes.clear()

# classify and print landing result. hard landing if v_y > 2 m/s
if -lander.vel.y > 2:
    formatted = "Hard landing ($v_y$ = {:.3f} $m/s$)".format(-lander.vel.y)
elif abs(lander.rad) < np.pi/6:
    formatted = "Safe landing ($v_y$ = {:.3f} $m/s$)".format(-lander.vel.y)
else:
    formatted = "Your ship is sideways ($v_y$ = {:.3f} $m/s$)".format(-lander.vel.y)

plotAxes.set_title(formatted, fontsize=15, color='white')

# print the result frame
landscape.plot(screenWidth, lander.pos.x)
lander.plot(thrust=0) # force-reset thrust to 0 to remove the gas graphics
controlPanel.plot()

plotAxes.set_xlim(lander.pos.x - screenWidth/2, lander.pos.x + screenWidth/2)
plotAxes.set_ylim(-10, screenHeight - 10)

formatted = "time taken = {0:.3f} $s$".format(totalTime) # this variable is to reduce the column size of the next line
plotAxes.annotate(formatted, xy=(0.01, 0.95), xycoords='axes fraction', color='white') # add total time annotation

'''
Small difference between 'totalTime' and the expected time taken (= 14.142) is from
the fact that it is not possible for the variable 'deltaTime' to be infinitely small
'''

plt.draw() # 'draw' to update axes title
plt.show() # 'show' to keep the screen on
