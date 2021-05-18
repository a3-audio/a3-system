# MOTION CONTROLLER

OSC TRANSMITTER AND PATTERNSAMPLER FOR 3-DIMENSIONAL AUDIO MOTION.

## OVERVIEW:

PLAYMODE
- PLAY
- RUNTIME-EDIT
    - Audio conversion mode (Mono, Stereo, VBAP, Ambisonic)
    - BPM
    - Width
    - Sides (3d-Boost)
    - Beat: musical rhythm notation (1/4, 1/8, 3/4...)
    - Bars: length of patternloop
- STOP

SETUPMODE
- SPEAKERSETUP
    - Select Preset
    - Edit Preset
        - Number of loudspeakers
        - Select loudspeaker
        - Adjust position: azimuth, distance, elevation
    - Save and load, ask to enter new name or overwrite
- HEADPHONESETUP
    - Headphone sounds more realistic with fitting hrtf filtercurve
    - Select and load Preset
- PATTERNEDITOR
    - Select bank
    - Edit bank: touch a row or pattern to open "select -> Save -> bank/row/pattern dialog""
    - Save /bank/row/pattern
    - Load selection to buttonmatrix
- OPTIONS
    - Brightness
    - IP-Address, PORT this device
    - IP-Address, PORT to receiver
    - Export settings to usb

## HARDWARE LAYOUT
```
 CH1 CH2 CH3 CH4
  |   |   |   |
  v   v   v   v
|---------------|
| W | W | W | W | <- POTIS FOR WIDTH
|---------------|
| S | S | S | S | <- POTIS FOR SIDES (3d-Boost)
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
| E | E | E | E | <- ENCODER
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

## DISPLAY LAYOUT
The touchscreen displays a lot of information but it makes sense in order 
to control and see all information on one fingertip.

```
       ch1            ch2           ch3            ch4        <- INFOFIELDS        
        |              |             |              |                 
        v              v             v              v                 
|-----------------------------------------------------------|         
| WIDTH:  -    | WIDTH:  30°  | WIDTH:  20°  | WIDTH:  30°  |         
| SIDES: -     | SIDES: +30dB | SIDES: +30dB | SIDES: 30+dB | 
|-----------------------------------------------------------|
|                            ch1                            |          
|                            sp2                            |
|                      __----ch2----__                      |
|                     L               R                     |
|                                                           |
|                                                           |
|                                                           |
|                                                           |
|  sp1                                                 sp3  |
|  ch1                                                 ch1  |
|                                                           |
|        R                                            L     |
|         |                                           |     | <- EAGLEVIEW: CURRENT SOUNDFIELD
|          |                                         |      |    
|         ch3                                       |       |    
|          |                                       ch4      |    
|           |                                       |       |
|            L                                     |        |
|                                                 |         |
|                                                 R         |
|                                                           |
|                                                           |
|                                                           |
|                                                           |
|             sp5                         sp4               |
|             ch1                         ch1               |
|                                                           |    
|-----------------------------------------------------------|         
| MODE:   MONO | MODE:   STER | MODE:   VBAP | MODE:   AMBI |         
| LENGTH: 34   | LENGTH: 34   | LENGTH: 34   | LENGTH: 34   |
| LOOP:   ONE  | LOOP:   LO0P | LOOP:   ONE  | LOOP:   ONE  |  
|-----------------------------------------------------------|    
| RCV:192.168.178.125:1234|SND:192.168.178.126:1232|BPM:128 | <- SYSTEMINFO
|-----------------------------------------------------------|

TOUCHDISPLAY LEGEND:
- INFOFIELD: COLORS - 4 channels, 4 infofield areas, 4 different colors
- INFOFIELD: MODE - The Stereosource will be converted to Mono, Stereo, Ambisonic
- INFOFIELD: WIDTH - How wide your sources spread in the sphere (exept monomode)
- INFOFIELD: SIDES - Boost the sideinformation of a stereotrack because this information is what does the impact in ambisonic - concider it as 3d-boost
- INFOFIELD: BPM - Calculated BPM for each Track, cool to run musicious motionpatterns
- INFOFIELD: BEAT - Map motionpatterns on estimated BPM
- INFOFIELD: BARS - Lenght of motionsequence

- EAGLEVIEW: SP - The speakerposition
- EAGLEVIEW: CH - The channelposition (channels are colorcoded)
- EAGLEVIEW: LR - The width of a stereosource

- SYSTEMVIEW: RCV - This device OSC input
- SYSTEMVIEW: SND - This device OSC output
- SYSTEMVIEW: BPM - Master BPM
```
## PLAYMODE
- Encoder 1-4: Push

### PLAYMODE: PLAY
- Encoder 1-4 Push: Toggle RUNTIME-EDIT Mode for this channel
- Encoder 1-4 Double Push: Enter Setup Page 1-4
- Buttonmatrix Push: play/pause pattern
- Buttonmatrix Double Push: toggle repeat 

### PLAYMODE: RUNTIME-EDIT
- Encoder - Push: Toggle through INFOFIELD-options
- Encoder - Turn: Adjust option
    - MODE: mono, stereo, vbap, ambisonic
    - BEAT: 1/4, 1/8, 1/16, 2/3, ... 
    - BARS: length of patternloop
    - WIDTH: Spread stereo
    - REVERB: Adjust reverblevel
- Touchdisplay onTouch: Records Motion to cachefile
- Touchdisplay onRelease: Plays Motion from cachefile
- Buttonmatrix long press: Stores cachefile to BUTTON
- Encorder Double Push: Exit to PLAYMODE

## SETUPMODE
Encoder 1-4: Double-Push. 

### SPEAKERSETUP: SELECT PRESET
Encoder 1: Double-Push
- Encoder 1 Turn: Select Preset - SELECT overlay
- Encoder 1 Push: Load Preset 

### SPEAKERSETUP: EDIT PRESET
Encoder 2: Double-Push
- Encoder 1 Turn: Set Number of outputs
- Encoder 2 Turn: Select output
- Encoder 3 Turn: Set Azimuth for selected output
- Encoder 4 Turn: Set Distance for selected output

### SPEAKERSETUP: SAVE AND LOAD
- Display Button SAVE: SAVE TO .. overlay
- Display Button DISCARD: Discard changes
- Display Button ENABLE: Upload Speakerlayout to Audioengine
- Display Button EXIT: Return to PLAYMODE and open dialog "save changes?" [yes, dismiss]
```
|-----------------------------------------------|
| SPEAKERSETUP                                  | <- SPEAKERSETUP: SELECT PRESET
| 5 CHANNEL CIRCLE WITH DISTANCE 4.5m           |
|-----------------------------------------------|
| OUTPUTS  |  SELECT   |  AZIMUTH  |  DISTANCE  | <- SPEAKERSETUP: EDIT PRESET
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
|   SAVE   |  DISCARD  |   ENABLE   |   EXIT    | <- SPEAKERSETUP: SAVE AND LOAD                   
|          |           |            |           |
------------------------------------------------|

SELECT and SAVE TO.. - OVERLAY
- Encoder 1 Turn: select
- Encoder 1 push: enter selection

|-----------------------------------------------|
| SPEAKERSETUP                                  |
| 5 CHANNEL CIRCLE WITH DISTANCE 4.5m           |
|-----------------------------------------------|
| OUTPUTS  |  SELECT   |  AZIMUTH  |  DISTANCE  |             
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

A common workflow, starting from PLAYMODE:
- Encoder 1: Double Push - enter SPEAKERSETUP
- Encoder 1: Turn - Select speakerlayout
- Encoder 1: Push - Edit speakerlayout
- Encoder 2: Double Push - enter SETUPMODE LEVEL 2
- Encoder 1: Turn - Adjust number of speaker outputs
- Encoder 2: Turn - Select speaker 1
- Encoder 3: Turn - Adjust Azimuth of speaker 1(-180°, 180°)
- Encoder 4: Turn - Adjust Distanz of speaker 2
- Repeat the last 3 steps for all your speaker
- Display Button SAVE: Save your speakerlayout
- Display Button ENABLE: Upload your setup to audioengine
- Display Button EXIT: Exit to PLAYMODE
```

### HEADPHONESETUP
Encoder 3: Double-Push
- Encoder 1 Turn: Select preset - SELECT overlay
- Encoder 1 Push: Enable preset

### PATTERNEDITOR: LAYOUT SELECT / EDIT
Encoder 4: Double-Push
- Encoder 1 Turn: Select BANK preset - SELECT overlay
- Encoder 1 Push: Load BANK preset to editor
- Encoder 2 Turn: Select ROW preset - SELECT Overlay
    - Encoder 1-4 Push: Load ROW to BANK
    - Encoder 1-4 Hold: Load ROW on BUTTONMATRIX
- Display Button PATTERN: Select PATTERN preset - SELECT overlay
    - Encoder 1 Turn: Select PATTERN preset
    - Encoder 1 Push: Load PATTERN preset to PATTERN

### PATTERNEDITOR: SAVE AND LOAD
- Display Button SAVE: SAVE TO .. overlay
- Display Button DISCARD: Discard changes
- Display Button ENABLE: Upload patternlayout to audioengine
- Display Button EXIT: Return to PLAYMODE and open dialog "save changes?" [yes, dismiss]

```
|-----------------------------------------------|
| PRESET BANK/ROW/PATTERN                       | <- LEVEL 3
| Presetbank: user                              |
|-----------------------------------------------|
|   ROW 1   |   ROW 2   |   ROW 3   |   ROW 4   | <- 
|-----------------------------------------------|
|           |           |           |           |
|  PATTERN  |  PATTERN  |  PATTERN  |  PATTERN  |
|           |           |           |           |
|-----------------------------------------------|
|           |           |           |           |
| 1/4 right |  PATTERN  |  PATTERN  |  PATTERN  |
|           |           |           |           |
|-----------------------------------------------| <- PREVIEW BUTTONMATRIXLAYOUT
|           |           |           |           | 
| 1/8 rand  |  PATTERN  |  PATTERN  |  PATTERN  |
|           |           |           |           |
|-----------------------------------------------|
|           |           |           |           |
| 1/16 diag |  PATTERN  |  PATTERN  |  PATTERN  |
|           |           |           |           |
|-----------------------------------------------|
|-----------------------------------------------|
|           |           |           |           |
|   SAVE    |  DISCARD  |  ENABLE   |   EXIT    |                                  
|           |           |           |           |
------------------------------------------------|

SELECT and SAVE TO.. - OVERLAY
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

PATTERNEDITOR BACKEND:
Example - Presetbank "smooth" 

Stored informations:
- Bankname
- Banklayout
- Rownames
- Rowlayouts
- Patternnames
- Patternconfig

If folder smooth contains a .ini file and subfolders, its a bank.
If it contains .ini file and .ptn files, its a row.

└── playlist1
└── playlist2
    ├── playlist1.ini
    ├── song1
    │   ├── layout.ini
    │   ├── drop.ptn
    │   ├── intro.ptn
    │   ├── steady.ptn
    │   └── woof.ptn
    ├── song2
    │   ├── layout.ini
    │   ├── drop.ptn
    │   ├── intro.ptn
    │   ├── steady.ptn
    │   └── woof.ptn
    ├── song3
    │   ├── layout.ini
    │   ├── drop.ptn
    │   ├── intro.ptn
    │   ├── steady.ptn
    │   └── woof.ptn
    └── song4
        ├── layout.ini
        ├── drop.ptn
        ├── intro.ptn
        ├── steady.ptn
        └── woof.ptn

A common Workflow starting from PLAYMODE:
- Encoder 3 Double push: Enter PATTERNEDITOR
- Encoder 1 Turn: Select presetbank
- Encoder 1 Push: Edit selected presetbank 
- Encoder 2 Turn: Select strip
- Display Button ROW 1-4: Load selected strip
- Encoder 3 Turn: Select pattern
- Display Button PATTERN: Load selected PATTERN
- Display Button SAVE: SAVE TO .. popup
- Display Button DISCARD: Discard changes
- Display Button ENABLE: Load current Layout to Buttonmatrix
- Display Button EXIT: Return to PLAYMODE and open dialog "save changes?" [yes, dismiss]

Note: Factorypresets are writeprotected but you can edit and store them as userpreset.
You can store motions in pattern, pattern in rows and rows in banks banks.
```

### OPTIONS
- Brightness
- IP-Address and Port Motioncontroller
- IP-Address and Port audioengine
- Export settings to usb

