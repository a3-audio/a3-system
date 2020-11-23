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
The Global Setup is multi-layered in "LEVELS". 
Toggle with Encoder 1-3: DOUBLE-Push. 

The Levels are:
- LEVEL 1: SPEAKERLAYOUT SELECT
- LEVEL 2: SPEAKERLAYOUT EDIT
- LEVEL 3: BUTTONMATRIX 

Note: Factorypresets are writeprotected but you can edit and store them as userpreset.
You can store motions in pattern and pattern in strips and patternbanks. 

```
A common workflow, starting from PLAYMODE:
- Encoder 1: Double Push - enter EDITMODE LEVEL 1
- Encoder 1: Turn - To select a speakerlayout
- Encoder 1: Push - To edit the layout
- Encoder 2: Double Push - enter EDITMODE LEVEL 2
- Encoder 1: Turn - Adjust number of speaker outputs
- Encoder 2: Turn - Select speaker 1
- Encoder 3: Turn - Adjust Azimuth of speaker 1(-180°, 180°)
- Encoder 4: Turn - Adjust Distanz of speaker 2
- Repeat the last 3 steps for all your speaker
- Display Button SAVE: Save your speakerlayout
- Display Button ENABLE: Upload your setup to audioengine
- Display Button EXIT: Exit to PLAYMODE
```

```
|-----------------------------------------------|
| SPEAKERLAYOUT                                 | <- LEVEL 1 
| 5 CHANNEL CIRCLE WITH RADIUS 4.5m             |
|-----------------------------------------------|
| OUTPUTS  |  SELECT   |  AZIMUTH  |  RADIUS    | <- LEVEL 2
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
|   SAVE   |  DISCARD  |   ENABLE   |   EXIT    | <- TOUCHBUTTONS                                  
|          |           |            |           |
------------------------------------------------|

LEVEL 1 - SPEAKERLAYOUT - PRESET SELECT
- Encoder 1 Turn: Select Preset
- Encoder 1 Push: Load Preset - SELECT popup

LEVEL 2 - SPEAKERLAYOUT - EDIT
- Encoder 1 Turn: Set Number of outputs
- Encoder 2 Turn: Select output
- Encoder 3 Turn: Set Azimuth for selected output
- Encoder 4 Turn: Set Radius for selected output

LEVEL 1+2 - SPEAKERLAYOUT - FINISH
- Display Button SAVE: SAVE TO .. popup
- Display Button DISCARD: Discard changes
- Display Button ENABLE: Upload current Speakerlayout to Audioengine
- Display Button EXIT: Return to PLAYMODE and open dialog "save changes?" [yes, dismiss]
```


```
SPEAKERLAYOUT - SELECT and SAVE TO.. - POPUP
- Encoder 1 Turn: select
- Encoder 1 push: enter selection

|-----------------------------------------------|
| SPEAKERLAYOUT                                 |              
| 5 CHANNEL CIRCLE WITH RADIUS 4.5m             |
|-----------------------------------------------|
| OUTPUTS  |  SELECT   |  AZIMUTH  |  RADIUS    |             
| 5        |  sp1      |  -80°     |  4.5m      |
|-----------------------------------------------|
|                                               |
|                     sp2                       |
|    |-------------------------------------|    |
|    |             Burning Man 2021        |    |
|    | selected -> GARBICZ 2019            |    |                        
|    |             Gardelegen 2018         |    |
|    |--------------------------------------    |  
|               sp5        sp4                  |
|                                               |
|                                               |
|-----------------------------------------------|
|-----------------------------------------------|
|          |           |            |           |
|   SAVE   |  DISCARD  |   ENABLE   |   EXIT    |                                                 
|          |           |            |           |
|-----------------------------------------------|
```

### EDITMODE: LEVEL 3 - BUTTONMATRIX - LAYOUT SELECT

```
A common Workflow starting from PLAYMODE:
- Encoder 3 Double Push: Enter EDITMODE - Level 3
- Encoder 1 Turn: Select presetbank
- Encoder 1 Push: Edit selected presetbank 
- Encoder 2 Turn: Select strip
- Display Button ROW 1-4: Load selected strip
- Encoder 3 Turn: Select pattern
- Display Button PATTERN: Load selected pattern
- Display Button SAVE: SAVE TO .. popup
- Display Button DISCARD: Discard changes
- Display Button ENABLE: Load current Layout to Buttonmatrix
- Display Button EXIT: Return to PLAYMODE and open dialog "save changes?" [yes, dismiss]
```

```
|-----------------------------------------------|
| BUTTONMATRIX PRESET BANK/ROW/PATTERN          | <- LEVEL 3
| Presetbank: user                              |
|-----------------------------------------------|
|   ROW 1   |   ROW 2   |   ROW 3   |   ROW 4   |
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

```
BUTTONMATRIX - SELECT and SAVE TO.. - POPUP
- Encoder 1 Turn: Select Buttonpattern
- Encoder 1 Push: Load Buttonpattern

|-------------------------------------------------|
| BUTTONMATRIX LAYOUT                             |  <- LEVEL 3
| USERSPACE 1                                     |
|-------------------------------------------------|
|   ROW 1   |   ROW 2    |   ROW 3    |   ROW 4   |
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
/ambijockey/moc/ch/1-4/vu/ [0-1]
/ambijockey/moc/ch/1-4/bpm/ [80-180]
/ambijockey/moc/master/bpm/ [80-180]
```
