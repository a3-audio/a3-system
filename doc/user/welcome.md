# A³ Pandemic
3D-Sound Dj-Setup with Live-Panning-Interface

## Design
A³ Pandemic is designed as dj-setup with 4 stereo input-channels and a tape-in for multichannel input. It is scalable and capable to feed up to 128 speakers in multiple 3d-sound-spheres.

It consists of three devices:

### A³ Core (The Sound-server)
A³ Core processes analog audio-signals, calculates 3d-sound-spheres and is remote-controlled by A³ Mix and A³ Motion (or any other osc-controller). A³ Core can handle a wide range of audio-hardware to fit environments like Dante, MADI or any class-compliant.
 
### A³ Mix (The DJ-Mixer)
A³ Mix is a DJ-Mixer with 3-band-kill-eq, fx-section for hi- and lopass, 3d-toggle, multichannel vu-meter and 3d-prelisten on headphones.
It has a „tape-in“ section for multichannel or stereo direct to mix bus.

### A³ Motion (The Motion-Sampler)
A³ Motion records motion from touchscreen, stores them on sample-pads and plays them back as loop, one-shot or different mode. A³ Motion handles loop-length, it syncs to bpm-clock, spreads stereo-width and boosts side from mid/side processing.
It is designed for dynamic live interaction with audio-panning in a 3d-sound-sphere while scratching tracks.

## Usecases:
- A³ Core encodes and decodes: You can preset your show with stereotracks and control-data. You can use [osccontrol-light](https://github.com/drlight-code/osccontrol-light) vst-plugin to send osc-data from inside daw.
- A³ Core decodes: You can pre-encode your show and just send 3rd order b-format (acn, sn3d)
- A³ Core just routes: You get discrete channels for each speaker
- A³ Core simulates speaker-setup: You can play direct out from Dolby or Auro-3D decoder
- A³ Triple: You use A³ Mix and A³ Motion with dj-players to scratch your tracks while moving them.

## Quickstart
- Plug in your instruments vinyl, cd, daw ..
- Plug in your speaker
- Put speakers in regular circle around center
- Plug CAT-cable from A³ Mix and A³ Motion to A³ Core
- Plug-In your headphones
- Power on

## In depth
- Asembly: [[assembly]]
- Configuration: [[configuration]]
- Development: [[development]]

## Goal for this project
- 3d-sound everywhere
- Community
- Compatibility
- Easy to use
- Flexibility
- Open-Source
- Quality
- Rock-Solid-Stable in runtime and housing
- Scalable

## Media
We put Media-files to [Seafile](https://tinycloud.lilbits.de/Media)

## Buy
- Get a custom-build set: 5500€ (without audio-hardware)
- Get it on Kickstarter: depends on community
- Build your own: ~1500€ (without audio-hardware)
- Buy audio-hardware: 750-35000€ (see [[parts]])
- Maintenance and Service Subscriptions: 100€ / Month

## Rent
- Rent A³ Pandemic set 325-650€ per day (without speakers)
- Rent A³ Speakers set  325-60000€ per Event (without show)
- Rent A³ Show 20000-350000€

## Git
A³ Pandemic Mainrepo:
https://github.com/ambisonics-audio-association/Ambijockey
A³ Motion UI-repo:
https://github.com/ambisonics-audio-association/MotionControllerUI

## Support
- Help-desk
- Community

## Contact
- [contact@orbitalwaves.net](mailto:contact@orbitalwaves.net)
- [mattermost](https://talk.lilbits.de/ambisonics)