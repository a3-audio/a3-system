This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

https://docs.platformio.org/en/latest/core/installation.html#system-requirements

to init penv:
virtualenv -p python3 ~/.platformio/penv

to enter penv:
source ~/.platformio/penv/bin/activate

platformio
----------

Board Identifier:
pio boards teensy

Initialize Project:
mkdir pathToProject
cd pathToProject
pio project init --board teensy41

run project:
pio run --target upload
