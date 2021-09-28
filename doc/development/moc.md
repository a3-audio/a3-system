# A³ Motion Developement
A³ Motion backend runs on ArchlinuxARM on a Raspberry 3b. As Microcontroller we're using Teensy 4.1. 

## UI
A³ Motion UI is the most potential and complex part to develop. It is in a different repository (see [[Ambijockey/doc/configuration/moc]]).

## Raspberry
Connected to:
- A³ Core (lan)
- Display (hdmi & usb)
- Teensy (serial usb)

Osc-communication:
- Send stereowidth
- Send stereosides boost
- Send azimuth/elevation
- Receive bpm

Script:
- ```Controller_Motion/software/MotionControllerUI/moc_ui.py```

## Teensy
Connected to:
- Mainboard
	- Encoder (gpio)
	- potis (ic: hc4051)
	- neoPixel (gpio)
	- Buttonmatrix (ic: SN74HCT245N)

Firmware:
- ```Controller_Motion/software/teensy/src/main.cpp```

## Audio
A³ Mix, as a good DJ-Mixer, must have a headphone-plug somewhere. We installed a headphone-amp which is bus-powered by usb. It receives linelevel analogsignal from audiohardware. We put the headphone-plug to the front and 2 xlr-sockets to the back.
