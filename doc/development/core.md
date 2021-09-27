# A³ Core Development

A³ Core runs archlinux and has the following tasks:
- 

## Python
server.py is the OSC-router 

## Supercollider VU-Meter
vu-meter.scd is a 12-Channel Jack to osc vu-meter for A³ Mix

## Reaper
pluginhost and mixerbackend

### Signalflow
Masterbus
```
receives    name                
--------------------------------
[1,2]       phonesbus           
[3]         monobus (single)    
[4]         subbus              
[5-20]      spare               
[21-inf]    monobus (multi)     
[21-inf]    stereobus           
[21-inf]    decoderbus          
```

Phonesbus
```
receives    name                
--------------------------------
[1,2]       monobus(ph)         
[1,2]       stereobus(ph)       
[1,2]       binauralbus(ph)     
-           dj1-pfl
-           dj2-pfl
-           dj3-pfl
-           dj4-pfl
-           mainmixbus
```

Reverbbus
```
receives    name                
--------------------------------
[1-16]      reverb              
[17-32]     reverb(ph)          
```

Channelbus
```
receives    name                
--------------------------------
-           input
-           mid
-           side
-           m/s
[1]         mono                
[2]         subwoofer           
[3,4]       stereo              
[5-20]      b-format            
[21]        mono(preF)          
[23,24]     stereo(preF)        
[25-40]     b-format(preF)      
```

Basechannels
```
receives    		name                
--------------------------------
([1,2], hw-in)     	input       
([1],   input)     	mid         
([2],   input)     	side        
([1,2]  mid, side) 	m/s         
([1,2]  m/s)       	mono        
([1,2], m/s)       	sub   
([1,2], m/s)       	stereo      
([1,2], m/s)       	b-format    
```
