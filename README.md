# A³ System
Interact live with 3D Audio

A³ Audio is a live 3D audio system for DJs and live acts. It places sound in an
ambisonics sound field and moves it round the room while the set is playing.
It is made of four parts:

- [A³ Core](https://a3-audio.github.io/a3-doc/user/a3core.html): the sound server.
- [A³ Mixer](https://a3-audio.github.io/a3-doc/user/a3mix.html): a 4-channel DJ mixer.
- [A³ Motion](https://a3-audio.github.io/a3-doc/user/a3motion.html): a motion sampler.
  It records movements on a touchscreen sphere and plays them back in time with the beat.
- [StemDeck](https://a3-audio.github.io/a3-doc/user/stemdeck.html): a stem player with
  two decks of four stems each.

This repository carries all of them as submodules, together with the
[beat-analyzer](https://a3-audio.github.io/a3-doc/user/beat-analyzer.html) and the docs.
One clone gives a set of states that belong together.

![The A³ Motion UI](https://a3-audio.github.io/a3-doc/_images/a3-motion-ui-display-one-clip.png)

**Everything else is in the documentation: https://a3-audio.github.io/a3-doc/**

## Stereo in, stems out

A CDJ gives you a finished stereo mix, and a stereo mix only moves as a whole.
StemDeck splits a stereo track into four stems itself: **drums, bass, other and
vocals**. Each stem then gets its own A³ channel and can travel the room on its
own path.

- **In:** stereo files, or a whole folder, dropped onto the library, or picked
  with **Create stems…**. FLAC, WAV, MP3, AIFF, OGG, M4A and Opus work.
- **Out:** one stem set per track, `Title - 1 - drums` to `Title - 4 - vocals`,
  in one target folder for the whole batch. A copy of the original goes into
  `originals/`.
- The stems keep the original's format. MP3, M4A and Opus become FLAC.
- The separation is [Demucs](https://github.com/adefossez/demucs) (`htdemucs`).
  It runs in the background on all cores but the audio thread's, so **the decks
  play on while a track is separated**.

![The StemDeck library with the Create stems… button](https://a3-audio.github.io/a3-doc/_images/stemdeck-library.png)

How to start it, what you get and the one-time setup:
[Making stems from a stereo track](https://a3-audio.github.io/a3-doc/user/stemdeck.html#stemdeck-stem-creator).

## Getting started

```bash
git clone https://github.com/a3-audio/a3-system ~/a3-system
~/a3-system/install
```

`install` asks which version (a tag) and which roles the machine has, then
checks out and installs only the parts those roles need. Each role names the
Debian packages it builds against; they are installed with one `apt-get` (through
`sudo`) before any role. Roles with a screen (Core, StemDeck, Motion UI) log
`aaa` in on tty1 and start X with i3 there, without a display manager, from the
next reboot on. `install --dry-run` shows what it would do. For now it
runs on Debian only, as the user `aaa`, from `/home/aaa/a3-system`.

A version is an annotated tag with the same name in every repository; this
repository's submodules record which commit of each belongs to it. See the
[release notes](https://a3-audio.github.io/a3-doc/ressources/release-notes.html).

## Pro DJ Link

StemDeck and the beat-analyzer work with Pro DJ Link: they follow the tempo
master of a Pro DJ Link network, and StemDeck can be that master when there is
no CDJ. Pro DJ Link and rekordbox are trademarks of AlphaTheta Corporation;
Pioneer DJ is a trademark of Pioneer Corporation. A³ is not affiliated with,
endorsed or certified by them. The support is an independent implementation for
interoperability, built from public documentation of the protocol. On a network
you do not run, ask the venue first. Details:
[Trademarks and Pro DJ Link](https://a3-audio.github.io/a3-doc/ressources/trademarks.html).

## Contributing

Care the docs, keep the code clean, and open a pull request against `main`.
Follow the [Contributor Covenant](https://contributor-covenant.org/) Code of Conduct.
Find us on stage.
