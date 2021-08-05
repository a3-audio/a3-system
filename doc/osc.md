© Copyright 2021 A³ Ambisonic Audio Adventures UG (Haftungsbeschränkt). 
This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

# OSC A³pandemics
All parameters are normalized to float [range 0-1] 

TODO talk about OSC conventions / suggestion by Jendrik:
- template: /ambijockey/ch/{#}/{controller}/{function}/.../{args}
- example: /ambijockey/ch/1/mixer/eq/mid/[0-1]

## A³core (server.py translates incoming osc and sends to daw)

| SOURCE | DESTINATION (Reaper) | Description |
| :------| :------------------- | :---------- |
| /ambijockey/mic/ch/1-4/gain | /track/i/gain | Channel i gain |       
| /ambijockey/mic/ch/1-4/hi | /track/i/fxeq/hishelf/gain | Channel i hi |         
| /ambijockey/mic/ch/1-4/mid | /track/i/fxeq/band/0/gain | Channel i mid |        
| /ambijockey/mic/ch/1-4/lo | /track/i/fxeq/loshelf/gain | Channel i low |
| /ambijockey/mic/ch/1-4/volume | /track/i/volume | Channel i volume |
| /ambijockey/mic/ch/1-4/mode | /track/i/mute | Channel i mode (Mono, Stereo, Ambisonic)
| /ambijockey/mic/master/volume | /track/i/volume | Master volume |
| /ambijockey/mic/master/booth | /track/i/volume | Booth volume |
| /ambijockey/mic/master/phMmix | /track/i/volume | Phones Mix |
| /ambijockey/mic/master/phVol | /track/i/volume | Phones volume |
| /ambijockey/mic/ch/1-4/pfl | /track/i/mute | Channel i pfl (even/odd) |
| /ambijockey/mic/ch/master/pfl | /track/i/mute | Master pfl (even/odd) |
| /ambijockey/moc/ch/1-4/width | /track/i/StereoEncoder/width | Range -360 / 360 |
| /ambijockey/moc/ch/1-4/sides | /track/i/sides | Channel i sides |
| /ambijockey/moc/ui/azimuth | [StereoEncoderPort]/azimuth | Range -180 / 180 |
| /ambijockey/moc/ui/elevation | [StereoEncoderPort]/elevation | Range -180 / 180 |


## A³mic (mic.py sends potis and knobs receives vu-meters)
- /ambijockey/mic/ch/1-4/pfl
- /ambijockey/mic/ch/1-4/gain
- /ambijockey/mic/ch/1-4/hi
- /ambijockey/mic/ch/1-4/mid
- /ambijockey/mic/ch/1-4/lo
- /ambijockey/mic/ch/1-4/volume
- /ambijockey/mic/ch/1-4/m1
- /ambijockey/mic/ch/1-4/m2
- /ambijockey/mic/ch/1-4/m3
- /ambijockey/mic/ch/master/pfl
- /ambijockey/mic/ch/master/volume
- /ambijockey/mic/ch/master/booth
- /ambijockey/mic/ch/master/phMix
- /ambijockey/mic/ch/master/phVol
- /vu/rcv/01-04 << input vu ff (peak/rms)
- /vu/rcv/05-12 << output vu ff (peak/rms)

## A³moc (serialAdapter.py)
- /ambijockey/moc/ch/1-4/motion/ xy [0-1]
- /ambijockey/moc/ch/1-4/width/ [0-1]
- /ambijockey/moc/ch/1-4/sides/ [0-1]
