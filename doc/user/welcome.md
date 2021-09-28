# A³ Pandemic
3D-Sound Dj-Setup with Live-Panning-Interface

## Design
A³ Pandemic is designed as dj-setup with 4 stereo input-channels and a tape-in for multichannel input. It is scalable and cappable to feed up to 128 speakers in multiple 3d-soundspheres.

It consits of three devices:

### A³ Core (The Soundserver)
A³ Core processes analog audiosignals, calculates 3d-soundspheres and is remotecontrolled by A³ Mix and A³ Motion (or any other osc-controller). A³ Core can handle a wide range of audiohardware to fit environments like dante, madi or any class-compliant.
 
### A³ Mix (The DJ-Mixer)
A³ Mix is a DJ-Mixer with 3-band-kill-eq, fx-section for hi- and lopass, 3d-toggle, multichannel vu-meter and 3d-prelisten on headphones.
It has a „tape-in“ section for multichannel or stereo direct to mix bus.

### A³ Motion (The Motion-Sampler)
A³ Motion records motion from touchscreen, stores them on samplepads and plays them back as loop, oneshot or different mode. A³ Motion handles looplength, it syncs to bpm-clock, spreads stereowidth and boosts side from mid/side processing.
It is designed for dynamic live interaction with audiopanning in a 3d-soundsphere while scratching tracks.

## Usecases:
- A³ Core encodes and decodes: You can preset your show with stereotracks and controlldata. You can use [osccontrol-light](https://github.com/drlight-code/osccontrol-light) vst-plugin to send osc-data from inside daw.
- A³ Core decodes: You can pre-encode your show and just send 3rd order b-format (acn, sn3d)
- A³ Core just routes: You get discrete channels for each speaker
- A³ Core simulates speakersetup: You can play direct out from dolby or auro-3d decoder
- A³ Tripple: You use A³ Mix and A³ Motion with dj-players to scratch your tracks while moving them.

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
We put Mediafiles to [Seafile](https://tinycloud.lilbits.de/Media)

## Buy
- Get a custom-build set for 5000€ (write us a message)
- Get it on kickstarter
- Build your own ~1500€ without audiohardware

## Git
A³ Pandemic Mainrepo:
https://github.com/ambisonics-audio-association/Ambijockey
A³ Moc UI-Repo:
https://github.com/ambisonics-audio-association/MotionControllerUI

## Support
- Help-desk
- Community

## Contact
- [contact@orbitalwaves.net](mailto:contact@orbitalwaves.net)
- [mattermost](https://talk.lilbits.de/ambisonics)