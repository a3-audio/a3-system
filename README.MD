# Ambijockey

Goal for this project is a Hardware Controller which enables everybody, who can use a dj-mixer, to perform
LIVE on a 3d-Audio-sphere (Ambisonic). You should consider it as loopmachine for panning motions. It
includes audiostream analysis to create a reliable live beatclock, wich let the user control step motions
out of bars, steps and bpm).

It consists of three elements:

- The Server which runs the audio and osc-routing-engine (live io-processing)
- The Mixercontroller: it looks like a 4-channel dj-mixer but just handles osc
- The Motioncontroller: the touchscreen records and shows actual position and width for all 4 stereo
  channels at the same time. Also it has 4 store/recall buttons and some potis/encoders for motionmodes
  and sequence parameters.

## Blackboard

### TODO`s

## dependencies

- Python3
- platformio
- [Reaper](https://www.reaper.fm/)
- [IEM Plug-in Suite](https://plugins.iem.at/)

## code of conduct

1. Don't panic

2. care the docs

3. keep the Code clean

4. Hinterlasse nichts, auser deiner Wurst.

5. Easter Eggs are welcome!

### git

To be simple we decided to use centralized workflow, described here:
https://www.git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows

1. Der Main Branch darf nicht direkt bearbeitet werden, die edits sollten immer in einem seperarten Branch gemacht werden und dann über ein pull requests zusammen gefügt werden. Die Ausnahmen bilden das [Balckboard](#Balckboard) in deiser README und die korektur von offensichtlichen Rechtschreibfehlern in der Doku.

2. wenn du dir ein eigenes Setup bauen willst, erstelle dir ein Forg, um es an dich anzupassen
