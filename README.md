©2021 A³ Ambisonic Audio Adventures UG (Haftungsbeschränkt). This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

# Ambijockey

![first ambijockey](doc/pix/gif1.gif)

## Goal for this project
Make venues and artists able to play 3D-Sound. The project aims for, easy to use spatialization interface, maximum flexibility and a price for everybody. Our first setup consists of three devices:

## A³core (The Audioserver)
The Audioserver is processing the analog audio, calculates the 3D-Soundsphere and is remotecontrolled via osc. Also it sends osc data with peak and rms information for vu-meters to the mixer. 

[A³core Readme](https://github.com/ambisonics-audio-association/Ambijockey/tree/main/Server#readme)

## A³mix (The DJ-Mixer)
The DJ-Mixer is an osc-controller. It sends osc to the Audioserver in order to manipulate 3-band-eq, volume, channelgain, etc. like a normal dj-mixer would behave. It has osc-controlled vu-meters for each input and for 8 outputs (you're free to map audiochannels on it)

[A³mix Readme](https://github.com/ambisonics-audio-association/Ambijockey/blob/main/Controller_Mixer/README.md)

## A³motion (The Motion-Sampler)
The Motion-Sampler is an osc-controller. It records and plays motion made by your fingertip on its touchscreen. We're using it to move audiosignals in a 3D-Soundsphere. You can hear the motion on headphones (activate corresponding pfl) and you can hear it on the main speakers - live interaction. Also it has samplerfunctionality like looplength, playmode, visual feedback and so on. It stores up to 4 different movements per channel, each on its own physical button.

[A³motion](https://github.com/ambisonics-audio-association/Ambijockey/blob/main/Controller_Motion/README.md)
[A³motion UI](https://github.com/ambisonics-audio-association/MotionControllerUI)

## Hardware
Parts we used are listed [here](https://github.com/ambisonics-audio-association/Businessplan/blob/main/recherche/parts.md)

## Blackboard
We organize our tasks in a [github-project](https://github.com/orgs/ambisonics-audio-association/projects/1)

We talk via [mattermost](https://talk.lilbits.de/ambisonics), and keep data in a seafilecloud, [write us](mailto:contact@orbitalwaves.net) to get involved.

We put Mediafiles to [Seafile](https://tinycloud.lilbits.de/Media).

## Contact
[contact@orbitalwaves.net](mailto:contact@orbitalwaves.net)

## Code of conduct
1. Don't panic
2. Care the docs
3. Keep the code clean
4. Eastereggs are welcome!

## Git
We use the centralized workflow, description [here](https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)

1. Don't edit the main branch. Use pull requests instead (if nobody reacts we're probably still mixing - find us on stage)
2. If you need an own different setup, forck this repo
