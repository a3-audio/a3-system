# Ambijocky Server README

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
