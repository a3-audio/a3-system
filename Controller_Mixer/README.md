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

## Start

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
