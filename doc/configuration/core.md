# A³ Core Configuration
Install Archlinux:
https://wiki.archlinux.org/title/Installation_guide

Follow the Professional_audio guide:
https://wiki.archlinux.org/title/Professional_audio

## Root operations on A³ Core
### Setup user
``` 
user-add -m aaa
groupadd realtime
usermod -aG realtime aaa
usermod -aG users aaa
usermod -aG audio aaa
usermod -aG video aaa

``` 
### Install depencies
```
nano /etc/pacman.conf
	[realtime]
	Server = https://pkgbuild.com/~dvzrv/repos/realtime/$arch

pacman -Syu

pacman -S linuxrt realtime-privileges rtirq python3 python python-osc jack2 qjackctl aj-snapshot iempluginsuite supercollider git python-pip

pip install numpy pyserial

install rtapp (from aur)

cd /home/aaa
git clone https://github.com/ambisonics-audio-association/Ambijockey.git

Download and activate reaper for Linux x86_64:
https://www.reaper.fm/download.php

- tar -xf 
- ./install-reaper.sh 

when prompt answer to install in /opt
```
### Copy files to corresponding system-folder:
```
/home/aaa/Ambijockey/Server/config/
├── etc
│   ├── dhcpcd.conf
│   ├── rtapp
│   │   └── rtapp.conf
│   ├── rtirq.conf
│   └── systemd
│       └── system
│           └── core.service
├── home
│   └── aaa
│       ├── .config
│       │   └── i3
│       │       ├── config
│       │       └── layout
│       │           ├── workspace-10.json
│       │           ├── workspace-7.json
│       │           ├── workspace-8.json
│       │           └── workspace-9.json
│       └── .xinitrc
├── usr
│   └── bin
│       └── aaa-connections.sh
└── .xinitrc
```
### Configure:
```
chmod +x /usr/bin/aaa-connections.sh
chmod +x /home/aaa/Ambijockey/Server/startup.sh
chmod a+rw /dev/ttyACM0
systemctl enable core
systemctl enable rtirq
systemctl enable rtapp

```
### Reboot