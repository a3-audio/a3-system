# © Copyright 2021 A³ Ambisonic Audio Adventures UG (Haftungsbeschränkt). 
# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

#!/bin/bash
python /home/aaa/Ambijockey/Server/server.py &
/usr/bin/sclang /home/aaa/Ambijockey/Server/supercollider/vu-meter.scd &
/usr/bin/non-mixer --osc-port 9002 /home/aaa/Ambijockey/Server/non-mixer/Ambijockey &
