# A³ Pandemic
3D-Sound Dj-Setup with Live-Panning-Interface

## Quickstart
- Plug your instruments vinylplayer, cd-deck .. to A³ Core inputs
- Plug your speaker in 
```
- ch 1 > A³ Mix L
- ch 2 > A³ Mix R
- ch 3 > Subwoofer
- ch 4-n > Satellite-Speakers from front-left clockwise
```
- Plug CAT-cable from A³ Mix to A³ Core
- Plug CAT-cable from A³ Motion to A³ Core
- Switch Mainpower on
- Plug-In your headphones
- Put on your Sunglasses

## Goal for this project
- Easy to use spatialization interface
- Maximum flexibility
- Best Quality
- Stability at runtime
- Community
- Open-Source
- Scalability
- Compatibility

## Devices
### A³ Core (The Audioserver)
The Audioserver is processing the analog audio, calculates the 3D-Soundsphere and is remotecontrolled via osc. Also it sends osc data with peak and rms information for vu-meters to the mixer.

Usecases:
* Case a) the core encodes and decodes. You insert your Vinyl/CD-Decks etc. 
* Case b) the core decodes your b-format-encoded audio
* Case c) the core relays discrete channels for each speaker
* Case d) the core simulates speakersetups for dolby or auro-3d
* Case e) the core and our dj-setup plus a-d as „tape-in“ with mode-selection and volume on A³mix

### A³ Mix (The DJ-Mixer)
The DJ-Mixer is an osc-controller. It sends osc to the Audioserver in order to manipulate 3-band-eq, volume, channelgain, etc. like a normal dj-mixer would behave. It has osc-controlled vu-meters for each input and for 8 outputs (you're free to map audiochannels on it)

### A³ Motion (The Motion-Sampler)
The Motion-Sampler is an osc-controller. It records and plays motion made by your fingertip on its touchscreen. We're using it to move audiosignals in a 3D-Soundsphere. You can hear the motion on headphones (activate corresponding pfl) and you can hear it on the main speakers - live interaction. Also it has samplerfunctionality like looplength, playmode, visual feedback and so on. It stores up to 4 different movements per channel, each on its own physical button.

## Usecases:
* Case a) the core encodes and decodes you send separated tracks & osc
* Case b) the core decodes your b-format-encoded audio
* Case c) the core gets discrete channels for each speaker
* Case d) the core simulates speakersetups for dolby or auro-3d
* Case e) the core and our dj-setup plus a-d as „tape-in“ with mode-selection and volume on A³mix

## Contact
- [contact@orbitalwaves.net](mailto:contact@orbitalwaves.net)
- [mattermost](https://talk.lilbits.de/ambisonics)

## Media
We put Mediafiles to [Seafile](https://tinycloud.lilbits.de/Media).

## Buy
- Get a custom-build set for 5000€ (write us a message)
- Get it on kickstarter

## Support
- For Custum-Build Customer
- From Community