https://docs.platformio.org/en/latest/core/installation.html#system-requirements

to start penv:
virtualenv -p python3 ~/.platformio/penv

platformio
----------

Board Identifier:
pio boards teensy

Initialize Project:
mkdir path_to_the_new_directory
cd path_to_the_new_directory
pio project init --board teensy41

run project:
pio run --target upload