# A³ Mix Configuration
## teensy
software/teensy/src/main.cpp << flash it on your teensy 4.1 (howto: /doc/teensy_flash_fw.md)

## Raspberry
- install raspbian
- clone Ambijockey repo

### requirements
- python3
- python-osc
- pip install numpy
- pip install process

### Start
~/mic.py

1. prepare a micro-sd card with raspberry os
2. put an empty file 'ssh' to boot-partition, this enables ssh
3. Boot Raspberry pi 4
4. search for your rasp ip-address ie: nmap -sn 192.168.1.0/24
5. ssh pi@192.168.1.x (pass= raspberry) 
6. Configure user
	sudo useradd -m aaa
	sudo passwd aaa
	sudo usermod -aG dialout aaa
	sudo usermod -aG users aaa
	sudo usermod -aG sudo aaa
	sudo usermod -aG gpio aaa
	exit
	ssh aaa@192.168.1.x
	sudo userdel pi
7. Update system
	sudo apt update
	sudo apt upgrade
8. sudo raspi-config
	3 Interface Options > P8 Remote GPIO > yes
9. Edit /boot/config.txt
	max_usb_current=1
10. Edit /boot/cmdline.txt
	logo.nologo (to the end of line)
11. install python
	python --version (check python version)
	  if not python3:
	    sudo su
	    update-alternatives --install /usr/bin/python python /usr/bin/python3 1
	    exit
  	    python --version (check python version)
	sudo apt install python3-numpy
	sudo apt install python3-pip
	pip3 install pyserial
	pip3 install python-osc
	pip3 install rpi_ws281x adafruit-circuitpython-neopixel
	python3 -m pip install --force-reinstall adafruit-blinka
12. Edit .bashrc
	export PATH="/home/aaa/.local/bin:$PATH"
13. Clone repo
	sudo apt install git
	git clone git@github.com:ambisonics-audio-association/Ambijockey.git
14. Setup service
	sudo cp Ambijockey/Controller_Mixer/software/raspberry/config/etc/systemd/system/mic.service /etc/systemd/system/
	sudo systemctl start mic.service
	sudo systemctl enable mic.service
	  if 'systemctl enable mic.service' throws an error 'invalid argument'
	    cd /etc/systemd/system/multi-user.target.wants
	    sudo ln -s /etc/systemd/system/mic.service
15. Setup static ip-address
	sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bck
	sudo touch /etc/dhcpcd.conf
	Edit /etc/dhcpcd.conf
	  interface eth0
	  static ip_address=192.168.43.51/24
	  static routers=192.168.43.1
	  static domain_name_servers=192.168.43.1 8.8.8.8
16. sudo apt purge bluez pi-bluetooth

Not shure if we need that. Should make some tests before:
13. fix for raspi random hold
	Edit /etc/sysctl.conf
	  Append:
	    vm.dirty_background_ratio = 5
	    vm.dirty_ratio = 10
