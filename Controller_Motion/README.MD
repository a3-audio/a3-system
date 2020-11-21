# Motion Controller

- E = Encoder
- W = Poti for Width
- R = Poti for Reverb
- B = Button to Rec and play Motion-Presets

```
-----------------
| E | E | E | E |
-----------------
-----------------
|               |
|               |
| TOUCHDISLPAY  |
|               |
|               |
-----------------
-----------------
| W | W | W | W |
-----------------
| R | R | R | R |
-----------------
-----------------
| B | B | B | B |
-----------------
| B | B | B | B |
-----------------
| B | B | B | B |
-----------------
| B | B | B | B |
-----------------
```

## Touchdisplay
```
---------------------------------------------------
|   ENC CH1  |  ENC CH2  |  ENC CH3  |  ENC CH4   |
|-----------.----------.---.------------.----------
| ch1 Mono |...........|...|.ch1        .         |          
| ch1 Wide |.          ..  . sp2        .         |
| ch1 Reve |.         L--..|.ch2------R .         |
|----------|.              .            .         |
| ch2 Ster |.             .            .          |
| ch2 Wide |.sp1        .         R   .       sp3 | 
| ch2 Rev  |-ch1      .           |  .        ch1.|
|----------|.       .            ch4.            .|
| ch3 VBAP |.      .              |              .|
| ch3 Wide |.   L-ch3-R           L              .|
| ch3 Rev  |.                                    .|
|----------|.                                    .|
| ch4 Ambi |.                                    .|
| ch4 Wide | .       sp5             sp4        . |
| ch4 Rev  |  .......ch1.............ch1........  |
|--------------------------------------------------
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
---------------------------------------------------
|   ENC CH1  |  ENC CH2  |  ENC CH3  |  ENC CH4   |
|--------------------------------------------------
|   OUTPUTS  |  SELECTED |  AZIMUTH  |  RADIUS    | <- LEVEL 1
|   5        |  1        |  -30°     |  7.5m      |
|--------------------------------------------------
|   PRESETSELECTION                               |
|   5 CHANNEL CIRCLE WITH RADIUS 3m               |
|                                                 |
|                    sp2                          |
|                                                 | <- LEVEL 2
|           sp1               sp3                 |
|                                                 |
|                                                 |
|               sp5      sp4                      |
|                                                 |
|--------------------------------------------------
|                        |                        |
|      SAVE & EXIT       |     DISCARD & EXIT     | <- LEVEL 3 IS ALWAYS TOUCHABLE   
|                        |                        |
---------------------------------------------------
```
## Global
- Button Longpress: Store Cache to Presetfile
- Button Shortpress: Plays Motion from Presetfile

