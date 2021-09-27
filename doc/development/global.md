# A³ Pandemic Development

## Audio
The Audiohardware could be any class-compliant or compatible madi/dante card. It is connected to A³ Core via PCIe or USB. Instruments, speakers, headphones and DJ-Gear are directly plugged into A³ Core's audiohardware.

A³ Core processes the inputsignal from audiohardware and outputs the calculated signal for headphones and speakers in spherical installation.

A³ Mix, as a good DJ-Mixer must have a headphone-plug somewhere. We put a headphone-amp in which is USB-Powered and receives linelevel analogsignal from audiohardware. We put the headphone-plug in front and 2 xlr on the back.

## Software-Architecture
A³ Core, A³ Mix, A³ Motion are connected via lan to the same network.
On each device runs a pythonscript which sends and receives OSC (Open Sound Control).

### A³ Core
#### Backend
A³ Core runs archlinux with a realtimekernel. It must be well tuned to get low latency and stable audiosignals.

Connected to:
- A³ Mix (lan)
- Audiohardware (PCIe, usb)
- FOH-Setup-Page (webfrontend) <- wip

Osc communication:
- Send to internal audio-engine
- Send to any external target (light- or video-engine)
- Send vu-meters to A³ Mix
- Receive poti and buttonstates from A³ Mix and A³ Motion (or any other osc-controller)
- Receive ambisonic-encoder parameters from A³ Motion (or any other osc-controller)

OSC-Router:
- ```Server/server.py```

### A³ Mix
A³ Mix backend runs a Raspbian on a Raspberry model 4b. As Microcontroller we're using the Teensy 4.1.

##### Raspberry
Connected to:
- A³ Core (lan)
- Teensy (serial usb)
- State-leds (neoPixel gpio)
- Headphones-amp (usb)

Osc communication:
- Receive peak and rms
- Send poti- and buttonstates 

Script:
-  ```Controller_Mixer/software/python/mix.py```

##### Teensy
Connected to:
- Mainboard
	- Potis (ic: hc4051)
	- Buttons (direct)
	- Fx- an modebuttons (ic: hc4051)
	- Vu-meters (neoPixel)

Firmware:
- ```aaa/Ambijockey/Controller_Mixer/software/teensy/mic/src/```

### A³ Motion
A³ Motion backend runs on ArchlinuxARM on a Raspberry 3b. As Microcontroller we're using Teensy 4.1. 

##### Raspberry
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

#### Teensy
Connected to:
- Mainboard
	- Encoder (gpio)
	- potis (ic: hc4051)
	- neoPixel (gpio)
	- Buttonmatrix (ic: SN74HCT245N)

Firmware:
- ```Controller_Motion/software/teensy/src/main.cpp```


- Usermanual: [[welcome]]