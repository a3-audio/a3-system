# A³core

## Static IP-Addresses
aaa-core 192.168.43.50 (audioserver)
aaa-mix 192.168.43.51 (mixer controller)
aaa-moc 192.168.43.52 (motion controller)

## Dependences

### sudo pacman -S 
realtime-privileges
rtirq
rtapp

python3 
python-osc

jack2
qjackctl
aj-snapshot
iempluginsuite 
sc

### git clone | chmod +x | move to /usr/local/bin
https://github.com/jacktrip/jmess-jack.git

### download | tar -xf | ./install-reaper.sh | opt
https://www.reaper.fm/download.php

### pip install
numpy 
pyserial

## Configuration
cp /etc/dhcpcd.conf /etc/dhcpcd-bck.conf
cp config/etc/dhcpcd.conf /etc/dhcpcd.conf
groupadd realtime
usermod -aG realtime aaa
usermod -aG audio aaa

## Need to flash Microcontroller via usb
sudo chmod a+rw /dev/ttyACM0
stat /dev/ttyACM0stat

## start
Server/server.py

## Hardware
- i5 quadcore with 3.2Ghz per Core
- ssd
- 8G Ram
- soundhardware could be everything what runs on linux. We use rme hdsp9652 because its cheap and works good for 24 analog io. We plugged a bunch of behringer dcx2496 behind and clocked it with a rosendahl nanoclock (64samples per package, 44100Hz, 16bit, 2.8ms roundtrip latency)

## OSC (server.py translates incoming osc and sends it to the daw)
TODO talk about OSC conventions / suggestion by Jendrik:
template: /ambijockey/ch/{#}/{controller}/{function}/.../{args}
exampel: /ambijockey/ch/1/mixer/eq/mid/[0-1]

SOURCE                          >>  DESTINATION
----------------------------------------------------------------------
CONTROLLER MIXER POTIS              REAPER
/ambijockey/mic/ch/1-4/gain         (Channel 1 gain)     >>  /track/15/ie/gain
/ambijockey/mic/ch/1-4/hi           (Channel 1 hi)       >>  /track/15/fxeq/hishelf/gain
/ambijockey/mic/ch/1-4/mid          (Channel 1 mid)      >>  /track/15/fxeq/band/0/gain
/ambijockey/mic/ch/1-4/lo           (Channel 1 low)      >>  /track/15/fxeq/loshelf/gain
/ambijockey/mic/ch/1-4/volume       (Channel 1 volume)   >>  /track/14/volume
/ambijockey/mic/ch/1-4/mode/ [0-2]  (Mono, Stereo, Ambisonic)

CONTROLLER MIXER POTIS              REAPER
/ambijockey/mic/master/volume        (Master volume)      >>  /master/volume
/ambijockey/mic/master/booth         (Booth volume)       >>  
/ambijockey/mic/master/phMmix        (Phones Mix)         >>  
/ambijockey/mic/master/phVol         (Phones volume)      >>  

CONTROLLER MIXER BUTTONS            REAPER
/ambijockey/mic/ch/1-4/pfl          (Channel 1 pfl)
/ambijockey/mic/ch/master/pfl

CONTROLLER MOTION POTIS
/ambijockey/moc/ch/1-4/width/ [0-1]
/ambijockey/moc/ch/1-4/sides/ [0-1]

CONTROLLER MOTION XYZ OR AZIMUTH
goes directly from moc.pc to corresponding encoder (each on a different port)
