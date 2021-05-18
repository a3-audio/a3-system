# Ambijockey

![first ambijocky](doc/pix/gif1.gif)

## Goal for this project
Make venues and artists fit for the future of audio. That means 3D-Sound and therefore compatibility to all audioformats, easy to use spatialization interface, and maximum flexibility at a price for everybody. Our first setup consists of three devices:

## A³core (The Audioserver)
The Audioserver is processing the analog audio, calculates the 3D-Soundsphere and is remotecontrolled via osc. Also it sends osc data with peak and rms information for vu-meters to the mixer. 

Server/README.md

## A³mix (The DJ-Mixer)
The DJ-Mixer is an osc-controller. It sends osc to the Audioserver in order to manipulate 3-band-eq, volume, channelgain, etc. like a normal dj-mixer would behave. It has osc-controlled vu-meters for each input and for 8 outputs (you're free to map audiochannels on it)

Controller_Mixer/README.md

## A³motion (The Motion-Sampler)
The Motion-Sampler is an osc-controller. It records and plays motion made by your fingertip on its touchscreen. We're using it to move audiosignals in a 3D-Soundsphere. You can hear the motion on headphones (activate corresponding pfl) and you can hear it on the main speakers - live interaction. Also it has samplerfunctionality like looplength, playmode, visual feedback and so on. It stores up to 4 different movements per channel, each on its own physical button.

Controller_Motion/README.md

## Hardware
Parts we used listed here: hardware.md

## Blackboard
We organize our tasks in a github-project:
https://github.com/orgs/ambisonics-audio-association/projects/1

We talk via mattermost, write us to get involved:
r.eismann@posteo.de

## Code of conduct
1. Don't panic
2. Care the docs
3. Keep the code clean
4. Eastereggs are welcome!

## Git
We use the centralized workflow, description here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Don't edit the main branch. Use pull requests instead (if nobody reacts we're probably still mixing - find us on stage)
2. If you need an own different setup, forck this repo
