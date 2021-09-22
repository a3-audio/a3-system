# OSC A³ Pandemic
All parameters are normalized to float [range 0-1] 

TODO talk about OSC conventions / suggestion by Jendrik:
- template: /ambijockey/ch/{#}/{controller}/{function}/.../{args}
- example: /ambijockey/ch/1/mixer/eq/mid/[0-1]

## A³ Core
### Server/server.py modifies and routes incoming osc to daw

| SOURCE | DESTINATION (Reaper) | Description |
| :------| :------------------- | :---------- |
| /mic/ch/1-4/gain | /track/i/gain | Channel i gain |       
| /mic/ch/1-4/hi | /track/i/fxeq/hishelf/gain | Channel i hi |         
| /mic/ch/1-4/mid | /track/i/fxeq/band/0/gain | Channel i mid |        
| /mic/ch/1-4/lo | /track/i/fxeq/loshelf/gain | Channel i low |
| /mic/ch/1-4/volume | /track/i/volume | Channel i volume |
| /mic/ch/1-4/mode | /track/i/mute | Channel i mode (Stereo, 3D)
| /mic/master/volume | /track/i/volume | Master volume |
| /mic/master/booth | /track/i/volume | Booth volume |
| /mic/master/phMmix | /track/i/volume | Phones Mix |
| /mic/master/phVol | /track/i/volume | Phones volume |
| /mic/ch/1-4/pfl | /track/i/mute | Channel i pfl |
| /mic/ch/master/pfl | /track/i/mute | Master pfl |
| /moc/ch/1-4/width | /track/i/StereoEncoder/width | Range -360 / 360 |
| /moc/ch/1-4/sides | /track/i/sides | Channel i sides |
| /moc/ui/azimuth | [StereoEncoderPort]/azimuth | Range -180 / 180 |
| /moc/ui/elevation | [StereoEncoderPort]/elevation | Range -180 / 180 |


## A³ Mix 
### potis and knobs (send)
- /mic/ch/1-4/pfl
- /mic/ch/1-4/gain
- /mic/ch/1-4/hi
- /mic/ch/1-4/mid
- /mic/ch/1-4/lo
- /mic/ch/1-4/volume
- /mic/ch/1-4/m1
- /mic/ch/1-4/m2
- /mic/ch/1-4/m3
- /mic/ch/master/pfl
- /mic/ch/master/volume
- /mic/ch/master/booth
- /mic/ch/master/phMix
- /mic/ch/master/phVol

### vu-meters (receive)
- /vu/rcv/01-04 << input vu ff (peak/rms)
- /vu/rcv/05-12 << output vu ff (peak/rms)

## A³ Motion
### potis, knobs and touch-xy (send)
- /moc/ch/1-4/motion/ xy [0-1]
- /moc/ch/1-4/width/ [0-1]
- /moc/ch/1-4/sides/ [0-1]

### bpm (receive)
