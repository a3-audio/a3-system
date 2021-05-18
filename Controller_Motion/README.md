# MOTION CONTROLLER
OSC TRANSMITTER AND PATTERNSAMPLER FOR 3-DIMENSIONAL AUDIO MOTION.

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

## OSC
``` 
# TRANSMIT
/ambijockey/moc/ch/1-4/motion/ xy [0-1]
/ambijockey/moc/ch/1-4/width/ [0-1]
/ambijockey/moc/ch/1-4/sides/ [0-1]

/ambijockey/moc/speakersetup/speakers [1-1024]
/ambijockey/moc/speakersetup/n/azimuth [-180-180]
/ambijockey/moc/speakersetup/n/Distance [m]
```
