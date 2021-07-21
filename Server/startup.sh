#!/bin/bash
python /home/aaa/Ambijockey/Server/server.py &
/usr/bin/sclang /home/aaa/Ambijockey/Server/supercollider/vu-meter.scd &
/usr/bin/non-mixer --osc-port 9002 /home/aaa/Ambijockey/Server/non-mixer/Ambijockey &
