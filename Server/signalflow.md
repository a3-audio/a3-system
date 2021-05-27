# Audio Signalfllow
Audio signalflow for ambijockey reaper project:

## masterbus 
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

## phonesbus
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

## reverbbus 
```
receives    name                
--------------------------------
[1-16]      reverb              
[17-32]     reverb(ph)          
```

## channelbus (per channel)(
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

## basechannels
```
input       ([1,2], hw-in)
mid         ([1],   input)
side        ([2],   input)
m/s         ([1,2]  mid, side)
mono        ([1,2]  m/s)
subwoofer   ([1,2], m/s)
stereo      ([1,2], m/s)
b-format    ([1,2], m/s)
```
