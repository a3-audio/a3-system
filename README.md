# A³ Audio
Interact live with 3D Audio

## System
- [A³ Core](https://a3-audio.github.io/a3-doc/user/a3core.html): 3D Sound Server (audio backend and analysis on reaper and supercollider)
- [A³ Mixer](https://a3-audio.github.io/a3-doc/user/a3core.html): 4-Channel DJ Mixer (osc controller)
- [A³ Motion](https://a3-audio.github.io/a3-doc/user/a3core.html): 4-Channel Motion Sampler (osc controller)
- [Beat-Analyzer](https://github.com/rafjagger/beat-analyzer.git): Real-time beat detection with JACK audio input and OSC output. Clock input support (Pioneer, A3-Motion) 

## Homepage
- https://a3-audio.github.io

## Documentation
- https://a3-audio.github.io/a3-doc

## Repository
- https://github.com/a3-audio/a3-system

## Code of conduct
- Care the docs
- Keep the code clean
- We use [centralized workflow](https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows):
  - Don't edit the mainbranch. Use pull requests instead.
  - If you need an own different setup, fork this repo
- Follow the <a href="https://contributor-covenant.org/">Contributor Covenant</a> Code of Conduct
- Find us on stage

## network ports (UDP/OSC)
```
| device    | program       | function        | RX    | TX    | description
| --------- | ------------- | --------------  | ----  | ----  | -----------
| a3-core   | a3-core.py    | -               | -     | -     | 
|           |               | receiver        | 8101  | -     | receive osc from a3-motion / a3-mixer
|           |               | DAW-control     | -     | 8102  | Sends to reaper
|           | beat-analyzer	| -               | -     | -     | analyze audio / receive pioneer clock / sends vu-meter, beatclock and bpm 
|           |               | a3-motion vu    | -     | 8111  | vu-meter 
|           |               | a3-motion beat  | -     | 8112  | beatclock and bpm 
|           |               | a3-mixer        | -     | 8113  | vu-meter
|           |               | lightjockey     | -     | 8114  | vu-meter
|           |               | lightjockey     | -     | 8115  | beatclock and bpm
|           |               | videojockey     | -     | 8116  | vu meter
|           |               | videojockey     | -     | 8117  | beatclock and bpm
|           |               | admin-pc        | -     | 8118  | vu-meter
|           |               | admin-pc        | -     | 8119  | beatclock and bpm
|           |               | pioneer dj link | 50000 | 50000 | announcing devices 
|           |               | pioneer dj link | 50001 | 50001 | beat synchronization
|           |               | pioneer dj link | 50002 | 50002 | detailed device status
|           | reaper        | DAW             | 8102  | -     | 
| a3-mixer  | a3-mixer.py   |                 | 8113  | 8101  | receive vu-meter, send parameter
| a3-motion | a3-motion-ui  |                 | 8111  | 8101  | receive vu-meter, send parameter
|           |               |                 | 8112  | -     | receive beatclock and bpm
```
