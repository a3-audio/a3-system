# MOTION CONTROLLER

OSC TRANSMITTER AND PATTERNSAMPLER FOR THE VERY SPECIAL PURPOSE OF 3-DIMENSIONAL AUDIO MOTION.

## HARDWARE LAYOUT

```
 CH1 CH2 CH3 CH4
  |   |   |   |
  v   v   v   v
|---------------|
| E | E | E | E | <- ENCODER
|---------------|
|               |
|               |
|               |
|               |
| TOUCHDISLPAY  | <- FANCY VISUALISATION OF CHANNELMOVEMENT
|               |
|               |
|               |
|               |
|---------------|
| W | W | W | W | <- POTIS FOR WIDTH
|---------------|
| R | R | R | R | <- POTIS FOR REVERB
|---------------|
| B | B | B | B | <- BUTTONS TO REC AND PLAY MOTION-PATTERNS
|---------------|    |
| B | B | B | B | <--|                        
|---------------|    |                 THE
| B | B | B | B | <--|            BUTTON-MATRIX 
|---------------|    |
| B | B | B | B | <--|
|---------------|
```

## PLAYMODE
The touchscreen displays a lot of information but it makes sense in order 
to control and see all information on one fingertip.

### PLAYMODE: ENCODER FUNCTIONS
- Encoder (1-4) Turn: Set audioconversion to Mono, Stereo, VBAP or Ambisonic for this channel
- Encoder (1-4) Push: Enable RUNTIME-EDIT Mode for this channel
- Encoder 1 and 2 Push together: Enter MAIN-EDITMODE

### PLAYMODE: RUNTIME-EDIT
- Encoder Turn: Change length of Recordloop for this channel
- Touchdisplay onTouch: Records Motion to cachefile
- Touchdisplay onRelease: Plays Motion from cachefile
- Buttonmatrix long Press: Stores cachefile to BUTTON
- Encorder Push: Disables RUNTIME-EDIT

```
       ch1            ch2           ch3            ch4                
        |              |             |              |                 
        v              v             v              v                 
|-----------------------------------------------------------|         
| MODE:   MONO | MODE:   STER | MODE:   VBAP | MODE:   AMBI |         
| BPM:    128  | BPM:    128  | BPM:    128  | BPM:    128  |
| WIDTH:  -    | WIDTH:  30°  | WIDTH:  20°  | WIDTH:  30°  |         
| REVERB: -    | REVERB: 30%  | REVERB: 30%  | REVERB: 30%  | <- INFOFIELD
| BEAT:   1/4  | BEAT:   1/4  | BEAT:   1/4  | BEAT:   1/4  |
| BARS:   4    | BARS:   4    | BARS:   4    | BARS:   4    |    
|-.----------.------------.--------------.----------.-------|
| .           .............|.ch1         .          .       |          
| .                         .sp2         .          .       |
| .                    __----ch2----__   .          .       |
| .                   L               R  .          .       |
| .                                      .          .       |
| .                                     ..          .       |
| .                                  ...            .       |
| .                               ...               .       |
| .sp1                         ...                  .  sp3  |
| -ch1                      ...                     .  ch1- |
| .                      ...                        .     . |
| .      R            ...                           . L   . |
| .       |        ...                              . |   . | <- EAGLEVIEW: CURRENT SOUNDFIELD
| .        |    ...                                 .|    . |    
| .       ch3...                                    |     . |    
| .        |                                       ch4    . |    
| .         |                                       |     . |
| .          L                                     |      . |
| .                                               |       . |
| .                                               R       . |
| .                                                       . |
| .                                                       . |
| .                                                       . |
| .                                                       . |
|  .          sp5                         sp4            .  |
|   ..........ch1.........................ch1............   |
|                                                           |    
||1-------2-------3-------4-------5-------6-------7-------| | <- RUNTIME-EDIT: PATTERNLENGTH   
||->->->->->->->->->                                      | | <- RUNTIME-EDIT: PATTERNPROGRESS
|-----------------------------------------------------------|    
| RCV:192.168.178.125:1234|SND:192.168.178.126:1232|BPM:128 | <- SYSTEMVIEW
|-----------------------------------------------------------|

TOUCHDISPLAY CONTENT

- INFOFIELD: COLORS - 4 channels, 4 infofield areas, 4 different colors
- INFOFIELD: MODE - The Stereosource will be converted to Mono, Stereo, VBAP or Ambisonic
- INFOFIELD: WIDTH - How wide your sources spread in the sphere (exept monomode)
- INFOFIELD: REVERB - An Ambisonic Reverb reflects from all directions (except monomode)
- INFOFIELD: BPM - Calculated BPM for each Track, cool to run musicious motionpatterns
- INFOFIELD: BEAT - Map motionpatterns on estimated BPM
- INFOFIELD: BARS - Lenght of motionsequenz

- EAGLEVIEW: SP - The speakerposition
- EAGLEVIEW: CH - The channelposition (channels are colorcoded)
- EAGLEVIEW: LR - The width of a stereosource
- EAGLEVIEW: .. - These thin colored lines connecting straight to corresponding infofield

- SYSTEMVIEW: RCV - This device OSC input
- SYSTEMVIEW: SND - This device OSC output
- SYSTEMVIEW: BPM - Master BPM
```

## EDITMODE: MAIN-SETUP
The Global Setup is multi-layered in "LEVELS". Toggle through with
Encoder 1-4: DOUBLE-Push. 

The Levels are:
- LEVEL 1: PRESET SPEAKERLAYOUT
- LEVEL 2: EDIT SPEAKERLAYOUT
- LEVEL 3: PRESET BUTTONMATRIX

BUTTONMATRIX: You can store your moves in patternpresets or presetbanks

Note: Factorypresets are writeprotected but you can edit and store them as userpreset.


### EDITMODE: LEVEL 1 - SPEAKERLAYOUT - PRESET SELECT
- Encoder 1 Turn: Select Preset
- Encoder 1 Push: Load Preset

### EDITMODE: LEVEL 2 - SPEAKERLAYOUT - EDIT
- Encoder 1 Turn: Set Number of outputs
- Encoder 2 Turn: Select output
- Encoder 3 Turn: Set Azimuth for selected output
- Encoder 4 Turn: Set Radius for selected output


```
|-----------------------------------------------|
| SPEAKERLAYOUT                                 | <- LEVEL 1 
| 5 CHANNEL CIRCLE WITH RADIUS 4.5m             |
|-----------------------------------------------|
| OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 2
| 5        |  sp1      |  -80°     |  4.5m      |
|-----------------------------------------------|
|                                               |
|                     sp2                       |
|        |sp1|                    sp3           |
|                                               |
|                                               | <- VISUALISATION OF SPEAKERSETUP
|                                               |
|                                               |  
|               sp5        sp4                  |
|                                               |
|                                               |
|-----------------------------------------------|
|-----------------------------------------------|
|          |           |            |           |
|  STORE   | ACTIVATE  |  DISCARD   |   EXIT    | <- TOUCHBUTTONS                                  
|          |           |            |           |
------------------------------------------------|
```

### EDITMODE: LEVEL 1/2 - EDIT SPEAKERLAYOUT
- Display Button STORE: Enter SPEAKERPRESET OVERLAY
- Display Button ACTIVATE: Loads current Speakerlayout into the Audioengine
- Display Button DISCARD: Recalls the current Preset into editor
- Display Button Exit: Returns to PLAYMODE and asks "do you want so save?" [yes, dismiss]

### EDITMODE: LEVEL 2 - SPEAKERLAYOUT - PRESET SELECT - OVERLAY
- Encoder 1 Turn: select userbank
- Encoder 1 push: overwrite userbank, enter presetname

```
|-----------------------------------------------|
| SPEAKERLAYOUT                                 | <- LEVEL 1 
| 5 CHANNEL CIRCLE WITH RADIUS 4.5m             |
|-----------------------------------------------|
| OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 2
| 5        |  sp1      |  -80°     |  4.5m      |
|-----------------------------------------------|
|                                               |
|                     sp2                       |
|    |-------------------------------------|    |
|    |             Burning Man 2021        |    |
|    | selected -> Garbicz 2019            |    | <- PRESET TO OVERWRITE 
|    |             Gardelegen 2018         |    |
|    |--------------------------------------    |  
|               sp5        sp4                  |
|                                               |
|                                               |
|-----------------------------------------------|
|-----------------------------------------------|
|          |           |            |           |
|  STORE   | ACTIVATE  |  DISCARD   |   EXIT    | <- TOUCHBUTTONS                                 
|          |           |            |           |
|-----------------------------------------------|
```

### EDITMODE: LEVEL 3 - BUTTONMATRIX - LAYOUT SELECT
- Encoder 1 Turn: Buttonmatrix Layout - Select Presetbank
- Encoder 1 Push: Load selected Presetbank to editor
- Display Button: Pattern - Enter BUTTONPATTERN EDITMODE
- Display Button: 

```
|-----------------------------------------------|
| BUTTONMATRIX LAYOUT                           | <- LEVEL 3
| Presetbank: user                              |
|-----------------------------------------------|
|           |           |           |           |
|  pattern  |  pattern  |  pattern  |  pattern  |
|           |           |           |           |
|-----------------------------------------------|
|           |           |           |           |
| 1/4 right |  pattern  |  pattern  |  pattern  |
|           |           |           |           |
|-----------------------------------------------| <- PREVIEW BUTTONMATRIXLAYOUT
|           |           |           |           | 
| 1/8 rand  |  pattern  |  pattern  |  pattern  |
|           |           |           |           |
|-----------------------------------------------|
|           |           |           |           |
| 1/16 diag |  pattern  |  pattern  |  pattern  |
|           |           |           |           |
|-----------------------------------------------|
|-----------------------------------------------|
|           |           |           |           |
|   SAVE    |    LOAD   |  DISCARD  |   EXIT    |                                  
|           |           |           |           |
------------------------------------------------|
```

### EDITMODE: LEVEL 3 - BUTTONPATTERN EDITMODE - OVERLAY
- Encoder 1 Turn: Select Buttonpattern
- Encoder 1 Push: Load Buttonpattern

```
|-------------------------------------------------|
| BUTTONMATRIX LAYOUT                             |  <- LEVEL 3
| USERSPACE 1                                     |
|-------------------------------------------------|
|           |            |            |           |
| 1/4 left  |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------|
|           |            |            |           |
| 1/4 |-------------------------------------|.    |
|     |             1/4 left                |     |
|-----| selected -> 1/4 RIGHT               |-----| <- PAD-SELECTION OVERLAY
|     |             1/8 random              |     |                           
| 1/8 |--------------------------------------.    |
|           |            |            |           |
|-------------------------------------------------|
|           |            |            |           |
| 1/16 left |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------|
|-------------------------------------------------|
|                        |                        |
|      SAVE & EXIT       |     DISCARD & EXIT     |                                  
|                        |                        |
--------------------------------------------------|
```

## GLOBAL STUFF
- Buttonmatrix Longpress: Store Cache to Presetfile
- Buttonmatrix Shortpress: Play Motion from Presetfile
- Poti 1-4 Reverb
- Poti 1-4 Width

## OSC
``` 
# TRANSMIT
/ambijockey/moc/ch/1-4/mode/ [0-3] (Mono, Stereo, VBAP, Ambisonic)
/ambijockey/moc/ch/1-4/motion/ xy [0-1]
/ambijockey/moc/ch/1-4/width/ [0-1]
/ambijockey/moc/ch/1-4/reverb/ [0-1]

/ambijockey/moc/master/speakerCount/n/ [1-24]
/ambijockey/moc/master/speakerPos/n/azimuth [-180-180]
/ambijockey/moc/master/speakerPos/n/Radius [m]

# RECEIVE
/ambijockey/moc/ch/1-4/motion/ xy [0-1]
/ambijockey/moc/ch/1-4/signal/ [0-1]
/ambijockey/moc/ch/1-4/bpm/ [80-180]
/ambijockey/moc/master/bpm/ [80-180]
```
