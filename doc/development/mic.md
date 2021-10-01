# A³ Mix Development
## A³ Mix
A³ Mix backend runs a Raspbian on a Raspberry Pi 4 Model B. As Microcontroller we're using the Teensy 4.1.

## Raspberry
Connected to:
- A³ Core (LAN)
- Teensy (serial usb)
- State-leds (neoPixel gpio)
- Headphones-amp (usb)

OSC communication:
- Receive peak and rms
- Send poti- and buttonstates 

Python-script:
-  ```Controller_Mixer/software/python/mix.py```

## Teensy
Connected to:
- Mainboard
	- Potis (ic: hc4051)
	- Buttons (direct)
	- Fx- an modebuttons (ic: hc4051)
	- Vu-meters (neoPixel)

Firmware:
- ```aaa/Ambijockey/Controller_Mixer/software/teensy/mic/src/```
