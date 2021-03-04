# Ambijockey

![first ambijocky](doc/pix/gif1.gif)

Goal for this project is a Hardware Controller which enables everybody, who can use a dj-mixer, to perform LIVE on a 3d-Audio-System. You can consider it as a loopmachine for pan-motions in all directions. 
It includes audiostream analysis to create a reliable live beatclock, wich let the user control step motions out of bars, steps and bpm.

It consists of three elements:

- Server: runs the audio and osc-routing-engine (live io-processing < 2.5ms)
- MixerController: seems to be a usual 4-channel dj-mixer but handles osc instead of audio
- MotionController: touchscreen record- loop and play interaction. Visualiser to show position and width for all 4 stereochannels at the same time. Also it has 4 store/recall buttons and some potis/encoders for motionmodes and sequence parameters.

## Blackboard

### TODO's

- beat-counter / beat-detection
- OSC looper
- MotionController
  - GUI
    - Motion-indicator für jeden Kanal
    - Farbe
    - OSC-Adressen eintragen
  - Dokumentation

### Hardware

Die Stecker die wie fur die Potis etc. wollen sind **JST XH 2.54mm**

- [WS2811 NeoPixel LED Driver Chip](https://www.adafruit.com/product/1378)
- [NeoPixel 5mm Through-Hole LED](https://www.adafruit.com/product/1938)
- [OLED Butten](https://www.alibaba.com/product-detail/Lakeview-DSP-OLED-LCD-Display-Screen_60759925392.html?spm=a2700.details.deiletai6.3.74dd7a76xJLr4l)
- [RGB Button](https://www.alibaba.com/product-detail/Lakeview-RGB-Full-Color-Momentary-Illuminated_60769825493.html?bypass=true)
- [RGB Tactile Button](https://www.alibaba.com/product-detail/Lakeview-TL3-RGB-Momentary-LED-Super_60769192488.html?spm=a2700.details.deiletai6.6.5a067a76Q1eRKz&bypass=true)
- [Tactile switch RGB](https://www.alibaba.com/product-detail/Tactile-switch-6x6-CHA-C602-series_1600146809793.html?spm=a2700.galleryofferlist.normal_offer.d_title.331e4785F4DJr6&s=p)

## dependencies

- Python3
- platformio
- [Reaper](https://www.reaper.fm/)
- [IEM Plug-in Suite](https://plugins.iem.at/)

## code of conduct

1. Don't panic

2. care the docs

3. keep the Code clean

4. Hinterlasse nichts, ausser deiner Wurst.

5. Easter Eggs are welcome!

### git

To be simple we decided to use centralized workflow, described here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Der Main Branch darf nicht direkt bearbeitet werden, die edits sollten immer in einem seperarten Branch gemacht werden und dann über ein pull requests zusammen gefügt werden. Die Ausnahmen bilden das [Balckboard](#Balckboard) in deiser README und die korektur von offensichtlichen Rechtschreibfehlern in der Doku.

2. wenn du dir ein eigenes Setup bauen willst, erstelle dir ein Forg, um es an dich anzupassen
