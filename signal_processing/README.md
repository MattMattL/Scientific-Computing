# Signal Processing Project

## Overview

The requirement of this project was to implement a fast Fourier transformation algorithm for general waves. The result of FFT can then be used to filter out certain frequency, etc.

My approach was to make a program with the visual of an oscilloscope. Features include:
* Can display Phase, Frequency and Adder mode on the screen.
* Scale buttons are used to zoom in/out on the phase/frequency plane.
* Windowing knobs are used to exclude some part of phase/frequencies.


## Demo

Choose a wave of your interest from the preset (sin, triangle, square, saw-tooth), or make your own.
![](../readme/signal_original.png)

Add random noise using the Add Noise button.
![](../readme/signal_noise.png)

Display the Frequency plane and filter out certain frequencies using the Masks dials.
![](../readme/signal_freq.png)

The filtered signal can be checked in the Phase mode.
![](../readme/signal_filtered.png)

Can also add new waves using the Add dials.
![](../readme/signal_add.png)