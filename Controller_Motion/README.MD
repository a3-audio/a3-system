# Motion Controller

```
 CH1 CH2 CH3 CH4
  |   |   |   |
  v   v   v   v
-----------------
| E | E | E | E | <- ENCODER
-----------------
-----------------
|               |
|               |
|               |
|               |
| TOUCHDISLPAY  | <- FANCY VISUALISATION OF CHANNELMOVEMENT
|               |
|               |
|               |
|               |
-----------------
-----------------
| W | W | W | W | <- POTIS FOR WIDTH
-----------------
| R | R | R | R | <- POTIS FOR REVERB
-----------------
-----------------
| B | B | B | B | <- BUTTONS TO REC AND PLAY MOTION-PRESETS
-----------------    |
| B | B | B | B | <--|
-----------------    |
| B | B | B | B | <--|
-----------------    |
| B | B | B | B | <--|
-----------------
```

## Touchdisplay
```
       ch1            ch2           ch3            ch4
        |              |             |              |
        v              v             v              v
-------------------------------------------------------------
| MODE:   MONO | MODE:   STER | MODE:   VBAP | MODE:   AMBI |
| WIDTH:  -    | WIDTH:  30°  | WIDTH:  20°  | WIDTH:  30°  |
| REVERB: -    | REVERB: 30%  | REVERB: 30%  | REVERB: 30%  |    
| BPM:    128  | BPM:    128  | BPM:    128  | BPM:    128  |
| BEAT:   1/4  | BEAT:   1/4  | BEAT:   1/4  | BEAT:   1/4  |
| BARS:   4    | BARS:   4    | BARS:   4    | BARS:   4    |    
|-.----------.------------.--------------.----------.--------
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
|------------------------------------------------------------
```
- Speakersymbol at Speakerposition with Outputnumber
- Sourceposition with thin lines to corresponding Encoder (Sources getting different colors)

## Playmode (per Channel)
- Encoder Turn: Changes Mode (Mono, Stereo, VBAP, Ambisonic)
- Encder Push (once): Enables Channel Editmode
- Encoder Push (twice): Enables Global Editmode

## Channel Editmode (per Channel)
- Encoder Turn: change lenght of Recordloop
- Touchdisplay onTouch: Records Motion to cachefile
- Touchdisplay onRelease: Plays Motion from cachefile

## Global Editmode
- Encoder 1 Push: Enter next Level
- Encoder 4 Push: Exit Global Editmode (do you want to save Setup?)
    - There are some common prebuild Setups (write protected)
    - And some userpresets (writable)

    ### Level 1
    - Encoder 1 Turn: Set Number of ouputs (speaker)
    - Encoder 2 Turn: Select output
    - Encoder 3 Turn: Set Azimuth for selected output
    - Encoder 4 Turn: Set Radius for selected output

    ### Level 2
    - Encoder 1 Turn: Select Preset
    - Encoder 1 Push: Load selected Preset
```
|--------------------------------------------------
|   OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 1
|   5        |  sp0      |  -80°     |  4.5m      |
|--------------------------------------------------
|                 PRESETSELECTION                 |
|         5 CHANNEL CIRCLE WITH RADIUS 3m         |
|                                                 |
|                       sp1                       |
|                                                 | <- LEVEL 2
|              sp0               sp3              |
|                                                 |
|                                                 |
|                  sp4      sp4                   |
|                                                 |
|--------------------------------------------------
|                        |                        |
|      SAVE & EXIT       |     DISCARD & EXIT     | <- LEVEL 3 IS ALWAYS TOUCHABLE   
|                        |                        |
---------------------------------------------------
```
## Global
- Button Longpress: Store Cache to Presetfile
- Button Shortpress: Play Motion from Presetfile

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
