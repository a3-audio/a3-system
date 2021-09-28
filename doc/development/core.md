# A³ Core Development
## Backend
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

## Supercollider VU-Meter.scd
Acts as 12-Channel Jack client and sends vu-meter (peak and rms) via osc to A³ Mix.

The supercollider projectfile:
- ```Server/supercollider/vu-meter.scd```

## Reaper Audioengine
A³ Core runs a jack2 audio-engine on top of alsa. Qjackctl may be used to patch virtual audio-cables from hardware to reaper and back out. Reaper acts as the mixer-backend which does the complex routing and user-interaction-tasks. It has a complex routing and bus-mapping described later. It processes the input-signal from audio-hardware and outputs calculated signals for headphones and speakers. The speaker must be placed in a most chubbiest spherical installation. Electronic corrections are possible for closer speakers.
Jmess is used to store and restore jack-connections, aj-snapshot is used to store and restore alsa-connections.

The Audiohardware could be any class-compliant or compatible Madi/Dante card. It is connected to A³ Core via PCIe or USB. Instruments, speakers, headphones and DJ-Gear are directly plugged into A³ Core's audiohardware.

The reaper pojectfile:
- ```Server/reaper/linux/reaper_ambijockey.RPP```

### Reaper bus-mapping
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