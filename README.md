# Ambijockey

![first ambijocky](doc/pix/gif1.gif)

## Goal for this project
Make venues and artists fit for the future of audioplayback. That means 3D-Sound and therefore compatibility to all audioformats, easy to use spatialization interface, and most flexibility at a price for everybody. Our first setup consists of three devices:

## The Audioserver
The Audioserver is processing the analog audio, calculates the 3D-Soundsphere and is remotecontrolled by osc. Also it sends osc data with peak and rms information for vu-meters to the mixer. 

Server/README.md

## The DJ-Mixer
The DJ-Mixer is a osc-controller. It sends osc to the Audioserver in order to manipulate 3-band-eq, volume, channelgain, etc. like a normal dj-mixer would behave. It has osc-controlled vu-meters for each input and for 8 outputs (you're free to map audiochannels on it)

Controller_Mixer/README.md

## The Motion-Sampler
The Motion-Sampler is a osc-controller. It records and playback motion made by fingertip on a touchscreen. We're using it to move audiosignals in a 3D-Soundsphere. You can hear the movement on headphones (by activating corresponding pfl) and you can hear it on the main speakers - live interaction. Also you can set parameters like lenghts or playmode, you can store 4 different movements per channel.

Controller_Motion/README.md

## Hardware
Parts we used are listed here: hardware.md

## Blackboard
We work with an agile Ticketboard integrated in github "projects".

https://github.com/orgs/ambisonics-audio-association/projects/1


## Code of conduct
1. Don't panic
2. care the docs
3. keep the Code clean
4. Easter Eggs are welcome!


## Git
To be simple we decided to use centralized workflow, described here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Don't edit the main branch. Use pull requests instead

2. If you need an own different setup forck this repo

3. Clone this repo:
git@github.com:ambisonics-audio-association/Ambijockey.git
