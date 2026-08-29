# A³ Audio
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

![A³ Motion UI](https://a3-audio.github.io/a3-doc/user/pics_user/a3-motion-ui-full.png)

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

The full address reference — every OSC message, its arguments and their ranges —
lives in the [OSC documentation](https://a3-audio.github.io/a3-doc/ressources/osc.html).

### Known inconsistencies

Worth knowing before chasing a silent link. These are recorded rather than fixed
because each needs a decision about which end is right:

- `a3-core.py` addresses its peers by **hardcoded IP** (`192.168.43.54`, `.55`), and
  `a3-mixer.py` does the same for the core (`192.168.43.50`). A system on a different
  subnet has those links dead with nothing to indicate it.
- `a3-core.py` sends to A³ Motion on port **8700**, while `a3-motion-ui` listens on
  **7771**.
- `beat-analyzer` is configured to reach the mixer on **7773/7774**, while
  `a3-mixer.py` listens on **7771**.

## Documentation

- Homepage: https://a3-audio.github.io
- Documentation: https://a3-audio.github.io/a3-doc
- This repository: https://github.com/a3-audio/a3-system

## Code of conduct

- Care the docs
- Keep the code clean
- We use [centralized workflow](https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows):
  - Don't edit the mainbranch. Use pull requests instead.
  - If you need an own different setup, fork this repo
- Follow the <a href="https://contributor-covenant.org/">Contributor Covenant</a> Code of Conduct
- Find us on stage
