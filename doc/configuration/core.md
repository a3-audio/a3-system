# A³ Core Configuration
Install Archlinux:
https://wiki.archlinux.org/title/Installation_guide

Follow the Professional_audio guide:
https://wiki.archlinux.org/title/Professional_audio


## Root operations on A³ Core
``` 
user-add -m aaa
groupadd realtime
usermod -aG realtime aaa
usermod -aG users aaa
usermod -aG audio aaa
usermod -aG video aaa

``` 

Install depencies
```
nano /etc/pacman.conf
	[realtime]
	Server = https://pkgbuild.com/~dvzrv/repos/realtime/$arch

pacman -Syu

pacman -S linuxrt realtime-privileges rtirq python3 python python-osc jack2 qjackctl aj-snapshot iempluginsuite supercollider git python-pip

pip install numpy pyserial

install rtapp (from aur)

git clone https://github.com/ambisonics-audio-association/Ambijockey.git /home/aaa


```

Download reaper for Linux x86_64:
https://www.reaper.fm/download.php

Install reaper:
```
- tar -xf 
- ./install-reaper.sh 
- when prompt answer to install in /opt
```

Copy files to corresponding system-folder:
```
/home/aaa/Ambijockey/Server/config/
├── aaa-connections.jmess
├── etc
│   ├── dhcpcd.conf
│   ├── rtapp
│   │   └── rtapp.conf
│   └── rtirq.conf
└── usr
    └── bin
        └── aaa-connections.sh
```

Configure:
```
chmod +x /usr/bin/aaa-connections.sh
chmod a+rw /dev/ttyACM0
systemctl enable server
```

