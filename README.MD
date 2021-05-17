# Ambijockey

![first ambijocky](doc/pix/gif1.gif)

## Goal for this project
Make venues and artists fit for the future of audioplayback. That means 3d-audio and therefore compatibility to all audioformats, easy to use spatialisation interface and most flexibility at low price. Our first setup consists of three devices:

## The Audioserver
The Audioserver is processing the analog audio, calculates the 3d-audiosphere and is remotecontrolled by osc. Also it sends osc data for vu-meters. 
To make this work you need a solid quadcore pc running a realtime linux kernel and a software/config-stack described in Server/README.md.

## The DJ-Mixer
The DJ-Mixer is just an osc-controller. It sends remotedata for eq volume gain and mix as osc to the Audioserver. It gets vu-meter levels as osc and displays it (4 in / 8 out).
The config is described in Controller_Mixer/README.md.

## The Motion-Sampler
The Motion-Sampler is an interface to record and playback controllerdata made with your fingertip on a touchscreen. We're using it to move audiosignals in a 3d-space. You can hear the movement during record on headphones and/or the main speakers, you can adjust parameters like lenghts or playbackmode, you can store 4 different movements per audiochannel.


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


## code of conduct

1. Don't panic

2. care the docs

3. keep the Code clean

4. Hinterlasse nichts, ausser deiner Wurst.

5. Easter Eggs are welcome!


### git

To be simple we decided to use centralized workflow, described here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Der Main Branch darf nicht direkt bearbeitet werden, die edits sollten immer in einem seperaten Branch gemacht werden und dann über ein pull requests zusammen gefügt werden. Die Ausnahmen bilden das [Blackboard](#Blackboard) in dieser README und die Korrektur von offensichtlichen Rechtschreibfehlern in der Doku.

2. wenn du dir ein eigenes Setup bauen willst, erstelle dir ein Forg, um es an dich anzupassen.

3. Adresse zum clonen:
git@github.com:ambisonics-audio-association/Ambijockey.git
