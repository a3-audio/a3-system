This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
© Copyright 2021 Raphael Eismann, Jendrik Bradaczek 

# A³mix
## Setup
### teensy
software/teensy/src/main.cpp << flash it on your teensy 4.1 (howto: /doc/teensy_flash_fw.md)

### Raspberry
- install raspbian
- clone Ambijockey repo

#### requirements
- python3
- python-osc
- pip install numpy
- pip install process

## Start
mic.py

## Hardware
- powered with PoE -> downstep to 3V inside
- runs on raspberry pi 3b
- raspberry is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 4 multiplexer hc4051 (8ch each)
        function: audiochannel-control
        potis
        - gain 
        - eq hi
        - eq mid
        - eq low
        - volume
        mode-buttons
        - mono
        - stereo
        - ambionic
    - 1 hc4051
        function: masterchannel-control
        potis
        - master volume
        - booth volume
        - phones mix
        - headphones volume
    - 5 led-buttons for heapdphones prelisten function (pfl)
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 3 leds mode-status
        - 9 leds input vu
    - 9 mode-buttons, 3 per channel
        - mono
        - stereo
        - 3d
    - 1 8x32 led-matrix for output-vu

## Open Sound Control (osc)
- receives osc messages from 
	- aaa-core/vu-meter.scd 
    - function: vu-meters
- sends osc messages to 
    - aaa-core/server.py
    - function: daw-controller, 4ch dj-mixer style
- messages /doc/osc.md
