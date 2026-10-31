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

This repository carries all of them as submodules, together with the docs; the
[beat-analyzer](https://a3-audio.github.io/a3-doc/user/beat-analyzer.html) comes
inside a3-core, the stem separator inside a3-stemdeck, and a3-pro-dj (the pro-DJ,
planned) sits beside them. One clone gives a set of states that belong together.

![Four StemDecks around the A³ desk and A³ Motion, each deck playing its own track](https://a3-audio.github.io/img/a3-setup.jpg)

**Everything else is in the documentation: https://a3-audio.github.io/a3-doc/**

## Stereo in, stems out

A CDJ gives you a finished stereo mix, and a stereo mix only moves as a whole.
The stems come from [**a3-stem-separator**](https://github.com/a3-audio/a3-stem-separator),
a separate tool that runs on your own computer, not on the rig: it splits each
stereo track into four stems on a rented cloud GPU and writes them as a stem set
StemDeck plays. Each stem then gets its own A³ channel and can travel the room
on its own path.

- **In:** FLAC, WAV or AIFF, single tracks or whole folders; finished tracks are
  skipped, an interrupted run continues.
- **Out:** one stem set per track, 44.1 kHz / 24-bit FLAC, by default the four
  stems `1 - low`, `2 - tops`, `3 - music`, `4 - vocals`, plus a copy of the
  original under `originals/`. Copy the library to the machines that play it.
- It shows the cost before it uploads anything.

How to set it up and run it: the
[a3-stem-separator README](https://github.com/a3-audio/a3-stem-separator#readme).

## Getting started

```bash
git clone https://github.com/a3-audio/a3-system ~/a3-system
~/a3-system/install
```

`install` asks which version (a tag) and which roles the machine has, then
checks out and installs only the parts those roles need. Each role names the
Debian packages it builds against; they are installed with one `apt-get` (through
`sudo`) before any role. Roles with a screen (Core, StemDeck, Motion UI, Desk) log
`aaa` in on tty1 and start X with i3 there, without a display manager, from the
next reboot on. The StemDeck role asks where the stem library is and hands the
path to StemDeck. The Desk role installs the virtual desk, the A³ Mixer on a
screen, as the app `a3-desk` from a3-mixer's pinned a3-mixer-ui (no service). The Core
role installs only on the machine that owns the Core
address in a3-core's `a3-osc.json` (or whose Core network answers set it): a second Core
would announce itself in the same LAN; the other roles install either way. `install --dry-run` shows what it would do. For now it
runs on Debian only, as the user `aaa`, from `/home/aaa/a3-system`.

By default the apps (a3-core, StemDeck, the UIs, the desk) come as packages
from the apt archive: no JUCE build, no submodule checkout beyond the
configuration. Which archive is `[system] archive = public|lan` in
`~/.config/a3/install.conf` (`public` is the GitHub archive and the default on a
fresh machine; `lan` is the rig's own apt source). A machine that is already
installed must name it once; without it the installer stops before any change,
also for a `--config FILE` run whose FILE has no `archive`.
`install --from-source` builds the apps from the pins as before, and is the only
way to install a named version: `install --from-source --update VERSION` (packages
mode refuses a version, the archive holds only the newest).

`install --ssh-key ~/.ssh/id_ed25519.pub` lets that public key log in as `aaa`
on a Core: the installer hands it to the `a3-core` package, which adds it to
`~/.ssh/authorized_keys` once. The file must hold exactly one public key line;
a private key or several lines stop the installer before anything is installed.
Without the option no key is added.

A role that was installed and is no longer ticked leaves the machine: its
services are stopped and disabled, the unit files the installer wrote are
removed, and for the Core the `a3-core` and `beat-analyzer` packages are removed
(not purged). The
installer lists exactly what goes and asks first; the answer defaults to no,
and the chosen roles install either way. Data, recordings, build folders,
`~/.config`, the packages installed for a role and group memberships stay; the
tty1 autologin stays too, even when no screen role is left. With no one to ask
(`--config FILE`, `--update`) a role leaves only when the settings file says
so under `[uninstall]`, `allow = yes`; otherwise the list is printed and the
role stays installed.

A version is an annotated tag with the same name in every repository; this
repository's submodules record which commit of each belongs to it.
`install --update` without a version keeps a machine on the branch it was set
to (`version = main` in `~/.config/a3/install.conf`), fast-forwarded to
origin's newest commit, and moves a machine on a tag to the newest tag;
`install --update v03.1` names one. See the
[release notes](https://a3-audio.github.io/a3-doc/ressources/release-notes.html).

## What's in A³ System

One version is one tag across every repository; the releases carry the notes
and the Debian packages: [releases](https://github.com/a3-audio/a3-system/releases).

```
A³ System                   the umbrella: installer, CI, pins  v03.2      GPL-3.0
├─ a3-core                  A³ Core and its window             v03.2      GPL-3.0
│  └─ a3-beat-analyzer      the beat clock                     v03.2      GPL-3.0
├─ a3-doc                   the documentation                  v03.2      CC-BY-SA-4.0
├─ a3-kicad-lib             the shared KiCad parts library     0652a57    CERN-OHL-S
├─ a3-mixer                 A³ Mixer                           v03.2      GPL-3.0
│  ├─ pcb                   the boards
│  │  ├─ v0_2               the built board                    rev v0.2   CERN-OHL-S
│  │  └─ v3_1               the V03 draft                      rev v3.1   CERN-OHL-S
│  ├─ housing               the housing                        rev v03.2  CERN-OHL-S
│  ├─ firmware              the board's firmware               rev v03.2  GPL-3.0
│  └─ a3-mixer-ui           the virtual desk                   v03.2      GPL-3.0
├─ a3-motion                A³ Motion                          v03.2      GPL-3.0
│  ├─ pcb                   the boards
│  │  ├─ v1                 the first boards                   rev v1     CERN-OHL-S
│  │  └─ v3_1               the current board                  rev v3.1   CERN-OHL-S
│  ├─ housing               the housing                        rev v03.2  CERN-OHL-S
│  ├─ firmware              the board's firmware               rev v03.2  GPL-3.0
│  └─ a3-motion-ui          the Motion UI                      v03.2      GPL-3.0
├─ a3-pro-dj                DJ knowledge, the autopilot        v03.2      GPL-3.0
├─ a3-stemdeck              the stem decks                     v03.2      GPL-3.0
│  └─ a3-stem-separator     the stems, made off the rig        v03.2      GPL-3.0
└─ third-party              what A³ is built on
   ├─ Airwindows            PurestGain, SmoothEQ3, Isolator3   2026-10    MIT
   ├─ BTrack                beat tracking                      1.0.7      GPL-3.0
   ├─ IEMPluginSuite        ambisonics encoder and decoders    v1.16.0    GPL-3.0
   ├─ JUCE                  the application framework          9.0.3      AGPL-3.0 OR JUCE-9
   ├─ kiss_fft              FFT inside BTrack                  1.3.0      BSD-3-Clause
   ├─ Neumann KU 100 HRIR   the binaural head                  2013       CC-BY-3.0
   ├─ platform-espressif32  the Motion board definition        2026-05    Apache-2.0
   └─ Roboto                the window's font                  1.100141   Apache-2.0
```

Every submodule sits at its repository's name, the nested ones inside the
repository that pins them, so `git clone --recurse-submodules` (or the
installer, which updates recursively) brings them along.

Code is GPL-3.0-or-later, boards and 3D-print files CERN-OHL-S-2.0, the
documentation CC-BY-SA-4.0; each repository's `.reuse/dep5` has the details.
Third-party works keep the licence their authors set; the a3-core window's
ABOUT page reads the same list from the checkout.

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
