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

## start
Server/server.py

## Hardware
- i5 quadcore with 3.2Ghz per Core
- ssd
- 8G Ram
- soundhardware could be everything what runs on linux. We use rme hdsp9652 because its cheap and works good for 24 analog io. We plugged a bunch of behringer dcx2496 behind and clocked it with a rosendahl nanoclock (64samples per package, 44100Hz, 16bit, 2.8ms roundtrip latency)

