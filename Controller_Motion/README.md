©2021 A³ Ambisonic Audio Adventures UG (Haftungsbeschränkt). This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

# A³motion
## Setup
### teensy
software/teensy/src/main.cpp << flash it on your teensy 4.1

### x86-sbc
- install a linux distro
- clone Ambijockey repo
	- put everything in etc to corresponding place
	- ToDo .xinitrc is missing in the homefolder yet
- clone MotionControllerUI repo
	- put MotionControllerUI/moc.sh to your home directory

#### requirements
- python3
- pyside6
- python-osc

## Start
- login
- startx
- ./moc.sh

## Hardware
- powered with PoE -> downstep to 3V inside
- runs on a x86-sbc
- sbc is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 1 multiplexer hc4051 (8ch)
        function: width and 3d-boost per channel
    - 2 hc4051
        function: Buttonmatrix
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 16 x status leds buttonmatrix

## Open Sound Control (osc)
- sends osc messages to 
    - aaa-core/encoder 1-4
    - function: asimuth
- messages /doc/osc.md
