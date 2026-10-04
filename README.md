# A³ System
Interact live with 3D Audio

A³ is a live spatial-audio instrument: three networked devices that let a performer
place and move sound in three dimensions while playing, rather than programming the
movement beforehand. Everything between the devices is OSC over UDP.

## System

| Device | Repository | What it is |
| :--- | :--- | :--- |
| [A³ Core](https://a3-audio.github.io/a3-doc/user/a3core.html) | [a3-core](https://github.com/a3-audio/a3-core) | 3D sound server — the machine that carries the audio. Debian x86_64 running JACK, REAPER and SuperCollider, remote-controlled over OSC. |
| [A³ Mixer](https://a3-audio.github.io/a3-doc/user/a3mix.html) | [a3-mixer](https://github.com/a3-audio/a3-mixer) | 4-channel DJ mixer. Sends gain, EQ, volume, PFL, FX and the 3D toggle; receives VU and LED state. |
| [A³ Motion](https://a3-audio.github.io/a3-doc/user/a3motion.html) | [a3-motion](https://github.com/a3-audio/a3-motion) · [a3-motion-ui](https://github.com/a3-audio/a3-motion-ui) | 4-channel motion sampler. Records movement trajectories on a touchscreen sphere and plays them back in time with the beat. |
| Beat-Analyzer | [beat-analyzer](https://github.com/rafjagger/beat-analyzer) | Real-time beat detection over JACK, plus the VU meters every device displays. Clock from its own analysis, from A³ Motion, or from Pioneer Pro DJ Link. |
| StemDeck | [stemdeck](https://github.com/rafjagger/stemdeck) | Stem player: two decks of four stems each. Any single stem can be sent to the aux bus on its own — and from there onto a movement. |

![A³ Motion UI](https://a3-audio.github.io/a3-doc/user/pics_user/a3-motion-ui-display.png)

## How the pieces talk

All three devices sit on one PoE Ethernet switch and speak **OSC over UDP**. Nothing
else passes between them.

```
   A³ Mixer ────── gain, EQ, volume, PFL, FX, 3D ──────▶ ┌──────────┐
                ◀──────────── VU, LED state ──────────── │          │
                                                         │ A³ Core  │──▶ REAPER
   A³ Motion ──── azimuth / elevation per channel ─────▶ │          │──▶ IEM plugins
                ◀──────────── VU, beat clock ─────────── └──────────┘
                                                              ▲
   Beat-Analyzer ── VU meters, beat, BPM ─────────────────────┘
                ◀── /beat, /tap, /clockmode ── A³ Motion
```

**A³ Core** computes the sound field. It receives parameters, turns them into
DSP settings, and drives REAPER and the IEM ambisonics plugins.

**A³ Motion** records where a sound should be and when. A finger draws a path on the
sphere; the path is stored as a pattern in ticks and played back at the clip's own
rate, in time with the beat clock.

**Beat-Analyzer** listens to the audio and produces the tempo everything else follows,
along with the VU meters that drive the visuals on A³ Motion.

**StemDeck** is where the music comes from. A Pioneer CDJ hands over a finished
stereo mix, and a stereo mix can only be moved as a whole. StemDeck plays two
decks of four stems each and sends any one of them to the aux bus on its
own. That is the step no DJ setup took before: a single part of the music,
picked out mid-set and handed to a movement. The vocal circles overhead while the groove stays
where it is. With A³ around it, this is the first complete DJ setup for 3D
sound.

StemDeck keeps its own time, too. It joins **Pioneer Pro DJ Link** as virtual
CDJ 6 and sends the beat of its MASTER deck there, so Beat-Analyzer (clock
mode 2) follows it exactly as it would follow a CDJ, and passes the beat on to
A³ Motion. With real CDJs on the link, StemDeck can follow them instead.

## Network ports (UDP/OSC)

The table below is what the running system actually uses, read out of each
component's configuration. Ports are configurable per device; these are the defaults
that ship.

| Component | Listens on | Sends to | Carries |
| :--- | :--- | :--- | :--- |
| **a3-core** (`a3-core.py`) | 9000 | REAPER `127.0.0.1:9001` | Channel, master and FX parameters in; DSP control out |
| | | IEM plugins `127.0.0.1:1337+n` | One port per ambisonics plugin instance |
| **a3-motion** (`a3-motion-ui`) | 7771 | a3-core `:9000` | Control: positions, channel parameters |
| | 7772 | | VU meters — a stream of its own, so it never shares a socket with the beat clock |
| | 7777 | | Energy grid from the IEM EnergyVisualizer (426 values) |
| | | beat-analyzer `:7775` | `/beat`, `/tap`, `/clockmode` |
| **a3-mixer** (`a3-mixer.py`) | 7771 | a3-core `:9000` | VU and LED state in; mixer parameters out |
| **beat-analyzer** | 7775 | a3-core `:9000`, a3-motion `:7771` / `:7772`, a3-mixer `:7773` / `:7774` | Beat and BPM out, VU meters out; external clock in |
| | Pioneer Pro DJ Link | 50000–50002 | Device announcement, beat sync, device status |
| **stemdeck** | Pioneer Pro DJ Link 50000–50002 | Pro DJ Link broadcast, as virtual CDJ 6 | Beat and status of its MASTER deck out; a CDJ's tempo in, for SYNC |

The full address reference — every OSC message, its arguments and their ranges —
lives in the [OSC documentation](https://a3-audio.github.io/a3-doc/ressources/osc.html).

### Known inconsistencies

Worth knowing before chasing a silent link. These are recorded rather than fixed
because each needs a decision about which end is right:

- `a3-core.py` addresses its peers by **hardcoded IP**, and `a3-mixer.py` does the
  same for the core (`192.168.43.50`). A system on a different subnet has those links
  dead with nothing to indicate it. Core's two can at least be pointed elsewhere
  without editing anything — `--mixer` and `--motion` — and the addresses in the file
  were finally corrected to the ones that answer (`.61:7772` for the mixer, measured)
  on 2026-09-12; they had been wrong in git for months while the working ones lived
  as a hand edit on the machine.
- `a3-core.py` sends to A³ Motion on port **8700**, while `a3-motion-ui` listens on
  **7771**.
- `beat-analyzer` is configured to reach the mixer on **7773/7774**, while
  `a3-mixer.py` listens on **7771**.

## Installing

Every machine of the system is set up from a clone of this repository, by
`install` -- the Core, a machine for StemDeck, the one the Motion PCB hangs
on. It asks which state of the system (a tag), which roles the machine has,
and their settings, then installs exactly that tag's submodules:

```bash
git clone --recurse-submodules https://github.com/a3-audio/a3-system ~/a3-system
~/a3-system/install
```

| Role | What it installs |
| :--- | :--- |
| A³ Core | the a3-core package, **built from this tag's a3-core** and held, so `apt upgrade` does not move it off the release; the beat-analyzer comes with it |
| StemDeck | StemDeck built in `stemdeck/`, its unit; on a machine without the Core also its zita units |
| Motion UI | Motion UI built in `a3-motion/ui/`, its unit, the group `dialout`, and the panel's firmware flashed when it changed |
| A³ Mixer | not yet (Raspberry Pi OS) |

The answers are kept in `~/.config/a3/install.conf`. A later run starts from
them; `install --update v03.1` takes them without asking and brings the
machine to that tag; `install --config FILE` sets up a second machine like
the first. `install --dry-run` shows every command and runs none.

For now it runs on Debian only, as the user `aaa`, from `/home/aaa/a3-system`:
the components' units name those paths. Windows and macOS come with the
first release that has packages for them.

## Repositories and versioning

**This section is the one place the project's shape is written down.** The
other repositories do not repeat it; they point here. A structure described in
eight places is a structure that will one day disagree with itself.

### What the pieces are

A³ is eight repositories and one system, and **this one carries the other seven
as submodules** — so a single clone brings a coherent set rather than whatever
each happened to be at that moment:

```
a3-system/                  the umbrella: this README, and the seven below
├── a3-core/                the sound server
├── a3-mixer/               the DJ mixer
├── a3-motion/              the motion sampler
│   └── ui/                 → a3-motion-ui, the touchscreen application
├── a3-doc/                 the documentation
├── a3-audio.github.io/     the homepage
├── beat-analyzer/          the beat clock and the VU meters
└── stemdeck/               the stem player
```

```bash
git clone --recurse-submodules https://github.com/a3-audio/a3-system
```

| Repository | What it holds |
| :--- | :--- |
| [a3-system](https://github.com/a3-audio/a3-system) | This: what the system is, how the pieces talk, how it is worked on. |
| [a3-core](https://github.com/a3-audio/a3-core) | The sound server as a Debian package tree — the OSC router, the SuperCollider backend, the REAPER project and its OSC surface, the systemd units. |
| [a3-mixer](https://github.com/a3-audio/a3-mixer) | The mixer's control scripts and its KiCad hardware. |
| [a3-motion](https://github.com/a3-audio/a3-motion) | The motion sampler's panel firmware and hardware. |
| [a3-motion-ui](https://github.com/a3-audio/a3-motion-ui) | The JUCE touchscreen application — the largest single piece of software here. Reached through a3-motion's `ui` submodule rather than a second time from this one: two gitlinks to one repository are two places to keep in step. |
| [a3-doc](https://github.com/a3-audio/a3-doc) | The user guide, the assembly photographs, and the **OSC reference every device is built against**. |
| [a3-audio.github.io](https://github.com/a3-audio/a3-audio.github.io) | The homepage. |
| [beat-analyzer](https://github.com/rafjagger/beat-analyzer) | The beat clock and the VU meters every device shows. Same system, different organisation — and versioned along with the rest. |
| [stemdeck](https://github.com/rafjagger/stemdeck) | The stem player: two decks of four stems, per-stem aux routing, its own Pro DJ Link clock. Like beat-analyzer, kept outside the organisation and versioned with the rest. |

### Work on `main`

**Development happens on `main` in every repository, and a version is a tag.**

Branch off `main` for a piece of work, merge it back into `main` when it is
done. Nothing else is an integration branch.

This replaced a scheme of one branch per hardware revision — `v03.2` in
a3-motion-ui, `dev/v03` in a3-mixer — which is the right shape when several
people ship revisions in parallel and the wrong one here. In practice one
person does most of the work, and `main` in a3-motion-ui fell **577 commits**
behind while everything real happened on the branch beside it. A branch nobody
integrates is not a release branch; it is a second `main` with a worse name.

Outside contributions are still pull requests against `main` — see the code of
conduct below. The rule above is about where the maintainers work, not an
invitation to push to somebody else's `main`.

### A version is a tag, and it is the same tag everywhere

A state worth returning to gets an **annotated tag**, set in **every
repository at once, with the same name**:

```
v03.0    2026-09-12    the first one
```

The same name everywhere is the whole point. These repositories only mean
something together — a Core that answers an address the Motion of a different
month never sends is not a system — so what you want when you go back is *the
eight states that belonged together*, and a single tag name is what finds them:

```bash
git clone --recurse-submodules https://github.com/a3-audio/a3-system
git -C a3-system checkout v03.0
git -C a3-system submodule update --init --recursive
```

The submodules are the same statement made a second way: this repository
records *which commit of each* belonged to that state, so a tag here brings
the whole set back even for anyone who never learned the convention.

Two rules that follow from that:

- **A tag is never moved.** Anyone who has already fetched it keeps the old
  one, so a moved tag means two people holding different things under one
  name. If the state was wrong, the next tag is the answer.
- **The number is the system's, not the repository's.** A repository with
  nothing to change since the last tag still gets the new one. That is not
  noise — it is the statement that this state belongs with the others.

`v03` is the hardware generation these tags sit in: the ESP32-S3 panel in
A³ Motion, the Raspberry Pi Pico mainboard in the mixer. The second number
counts states within it.

## Documentation

- Homepage: https://a3-audio.github.io
- Documentation: https://a3-audio.github.io/a3-doc
- This repository: https://github.com/a3-audio/a3-system

## Code of conduct

- Care the docs
- Keep the code clean
- We use [centralized workflow](https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows):
  - Contributing from outside: don't edit `main` directly — open a pull request.
    (The maintainers work on `main`; see *Repositories and versioning* above.)
  - If you need an own different setup, fork this repo
- Follow the <a href="https://contributor-covenant.org/">Contributor Covenant</a> Code of Conduct
- Find us on stage
