# MIXER CONTROLLER

## Setup

### teensy
software/teensy/src/main.cpp << flash it on your teensy 4.1

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

## OSC
``` 
# TRANSMIT
/ambijockey/mic/ch/1-4/pfl
/ambijockey/mic/ch/1-4/gain
/ambijockey/mic/ch/1-4/hi
/ambijockey/mic/ch/1-4/mid
/ambijockey/mic/ch/1-4/lo
/ambijockey/mic/ch/1-4/volume
/ambijockey/mic/ch/1-4/m1
/ambijockey/mic/ch/1-4/m2
/ambijockey/mic/ch/1-4/m3

/ambijockey/mic/ch/master/pfl
/ambijockey/mic/ch/master/volume
/ambijockey/mic/ch/master/booth
/ambijockey/mic/ch/master/phMix
/ambijockey/mic/ch/master/phVol

# RECEIVE
/vu/01-04 << input vu ff (peak/rms)
/vu/05-12 << output vu ff (peak/rms)
```

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
        - master-volume
        - booth-volume
        - phones mix
        - no headphone volume here!?:
            we feed line-level to builtin headphone-amplifier and control it analog
    - 5 led-buttons for heapdphones prelisten function (pfl)
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 3 leds mode-status
        - 9 leds input vu
    - 9 mode-buttons, 3 per channel
        - mono
        - stereo
        - 3d
    - 1 8x32 led-matrix for output-vu
- Open Sound Control (osc)
    - receives osc messages from 
        - aaa-core/vu-meter.scd 
        - function: vu-meters
    - sends osc messages to 
        - aaa-core/server.py
        - function: daw-controller, 4ch dj-mixer style
