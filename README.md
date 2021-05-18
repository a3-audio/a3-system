# Ambijockey

![first ambijocky](doc/pix/gif1.gif)

## Goal for this project
Make venues and artists fit for the future of audioplayback. That means 3d-audio and therefore compatibility to all audioformats, easy to use spatialization interface, and most flexibility at low price. Our first setup consists of three devices:

## The Audioserver
The Audioserver is processing the analog audio, calculates the 3d-audiosphere and is remotecontrolled by osc. Also it sends osc data with peak and rms information for vu-meters to the mixer. 

Server/README.md

## The DJ-Mixer
The DJ-Mixer is a osc-controller. It sends osc to the Audioserver in order to manipulate 3-band-eq, volume, channelgain, etc. like a normal dj-mixer would behave. It has osc-controlled vu-meters for each input and for 8 outputs (you're free to map audiochannels on it)

Controller_Mixer/README.md

## The Motion-Sampler
The Motion-Sampler is a osc-controller. It records and playback motion made by fingertip on a touchscreen. We're using it to move audiosignals in a 3d-audiosphere. You can hear the movement on headphones (by activating corresponding pfl) and you can hear it on the main speakers - live interaction. Also you can set parameters like lenghts or playmode, you can store 4 different movements per channel.


## Blackboard
We work with an agile Ticketboard integrated in github "projects".

https://github.com/orgs/ambisonics-audio-association/projects/1


## Code of conduct
1. Don't panic
2. care the docs
3. keep the Code clean
4. Hinterlasse nichts, ausser deiner Wurst.
5. Easter Eggs are welcome!


## Git
To be simple we decided to use centralized workflow, described here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Der Main Branch darf nicht direkt bearbeitet werden, die edits sollten immer in einem seperaten Branch gemacht werden und dann über ein pull requests zusammen gefügt werden. Die Ausnahmen bilden das [Blackboard](#Blackboard) in dieser README und die Korrektur von offensichtlichen Rechtschreibfehlern in der Doku.

2. wenn du dir ein eigenes Setup bauen willst, erstelle dir ein Forck.

3. Clone this repo:
git@github.com:ambisonics-audio-association/Ambijockey.git
