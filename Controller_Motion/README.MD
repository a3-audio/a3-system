# MOTION CONTROLLER

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
| B | B | B | B | <- BUTTONS TO REC AND PLAY MOTION-PRESETS
|---------------|    |
| B | B | B | B | <--|                        
|---------------|    |                THE
| B | B | B | B | <--|            BUTTONMATRIX 
|---------------|    |
| B | B | B | B | <--|
|---------------|
```

## PLAYMODE

### TOUCHDISPLAY CONTENT IN PLAY MODE
Placeholder for a Speakersymbol with Outputnumber inside is "sp". Also the Position of 
each stereosource is connected with thin lines to corresponding Infospace. Those lines 
are colorcoded and should go straight.

```
       ch1            ch2           ch3            ch4
        |              |             |              |
        v              v             v              v
|-----------------------------------------------------------|
| MODE:   MONO | MODE:   STER | MODE:   VBAP | MODE:   AMBI |
| WIDTH:  -    | WIDTH:  30°  | WIDTH:  20°  | WIDTH:  30°  |
| REVERB: -    | REVERB: 30%  | REVERB: 30%  | REVERB: 30%  |    
| BPM:    128  | BPM:    128  | BPM:    128  | BPM:    128  |
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
| .       |        ...                              . |   . |
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
|-----------------------------------------------------------|
```


### ENCODER FUNCTIONS IN PLAYMODE
- Encoder (1-4) Turn: Changes Mode (Mono, Stereo, VBAP, Ambisonic)
- Encder (1-4) Push: Enables RUNTIME-EDIT

#### RUNTIME-EDIT
- Encoder Turn: change lenght of Recordloop
- Encorder Push: Disables RUNTIME-EDIT
- Touchdisplay onTouch: Records Motion to cachefile
- Touchdisplay onRelease: Plays Motion from cachefile
- Buttonmatrix long Press: Stores Motion to PAD


## GLOBAL EDITMODE (PUSH ENCODER 1 TWICE TO ENTER) 
The Global Editmode is multi-layered in "LEVELS". Toggle through them with Encoder 1: DOUBLE-Push.

On some Pages you will select writeprotected factorypresets. Edit them and store as userpreset after.

### LEVEL 1/2 SPEAKERLAYOUT PRESET SELECTION AND EDIT
#### Level 1 (Select Speakerlayout-Preset)
- Encoder 1 Turn: Select Preset
- Encoder 1 Push: Load Preset

#### Level 2 (Edit Speakerlayout)
- Encoder 1 Turn: Set Number of ouputs (speaker)
- Encoder 2 Turn: Select output
- Encoder 3 Turn: Set Azimuth for selected output
- Encoder 4 Turn: Set Radius for selected output

#### TOUCHBUTTONS
- STORE: "PRESETSELECTION OVERLAY"
- ACTIVATE: Loads current Speakerlayout into the Audioengine
- DISCARD: Recalls the current Preset into editor
- Exit: Asks "do you want so save?" [yes, dismiss]

```
|-----------------------------------------------|
| SPEAKERLAYOUT PRESETSELECTION                 | <- LEVEL 1 
| 5 CHANNEL CIRCLE WITH RADIUS 3m               |
|-----------------------------------------------|
| OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 2
| 5        |  sp1      |  -80°     |  4.5m      |
|-----------------------------------------------|
|                                               |
|        _____        sp2                       |
|        |sp1|                    sp3           |
|        -----                                  |
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

#### PRESETSELECTION OVERLAY
- Encoder 1 Turn: select userbank
- Encoder 1 push: overwrites userbank (Ask for new Name)

```
|-----------------------------------------------|
| SPEAKERLAYOUT PRESETSELECTION                 | <- LEVEL 1 
| 5 CHANNEL CIRCLE WITH RADIUS 3m               |
|-----------------------------------------------|
| OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 2
| 5        |  sp1      |  -80°     |  4.5m      |
|-----------------------------------------------|
|                                               |
|                     sp2                       |
|    |-------------------------------------|    |
|    |             Userbank 1              |    |
|    | selected -> USERBANK 2              |    | <- PRESET TO OVERWRITE 
|    |             Userbank 3              |    |
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

### Level 3
- Encoder 1 Turn: Select Buttonmatrix-Preset (This Preset loads patterns for all PADS)
- Encoder 1 Push: Load selected Buttonmatrix-Preset to BUTTONMATRIX
- Display, Touch PAD: Enter PAD-Selection overlay

```
|-------------------------------------------------|
| BUTTONMATRIX PRESETSELECTION                    | <- LEVEL 3
| USERSPACE 1                                     |
|-------------------------------------------------|
|           |            |            |           |
| 1/4 left  |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------|
|           |            |            |           |
| 1/4 right |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------| <- PREVIEW BUTTONMATRIXLAYOUT
|           |            |            |           | 
| 1/8 rand  |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------|
|           |            |            |           |
| 1/16 left |    ...     |    ...     |    ...    |
|           |            |            |           |
|-------------------------------------------------|
|-------------------------------------------------|
|           |            |            |           |
|   SAVE    |    LOAD    |  DISCARD   |   EXIT    |                                  
|           |            |            |           |
--------------------------------------------------|
```

### PAD-Selection overlay 
- Encoder 1 Turn: Select PAD-Patch

```
|-------------------------------------------------|
| BUTTONMATRIX PRESETSELECTION                    |  <- LEVEL 3
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

## Global
- Buttonmatrix Longpress: Store Cache to Presetfile
- Buttonmatrix Shortpress: Play Motion from Presetfile

# OSC
``` 
## TRANSMIT
/ambijockey/moc/ch/1-4/mode/ [0-3] (Mono, Stereo, VBAP, Ambisonic)
/ambijockey/moc/ch/1-4/motion/ xy [0-1]
/ambijockey/moc/ch/1-4/width/ [0-1]
/ambijockey/moc/ch/1-4/reverb/ [0-1]

/ambijockey/moc/master/speakerCount/n/ [1-24]
/ambijockey/moc/master/speakerPos/n/azimuth [-180-180]
/ambijockey/moc/master/speakerPos/n/Radius [m]

## RECEIVE
/ambijockey/moc/ch/1-4/motion/ xy [0-1]
/ambijockey/moc/ch/1-4/signal/ [0-1]
/ambijockey/moc/ch/1-4/bpm/ [80-180]
/ambijockey/moc/master/bpm/ [80-180]
```
