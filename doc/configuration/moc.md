# A³ Motion Configuration
## teensy
software/teensy/src/main.cpp << [[flashTeensy]]

## Raspberry
Rapha:
We don't use raspberry cause pyside6 isn't compiled for arm at the moment. 
Waiting ... and use x68-architecture instead ...
2021-09-17 found pyside6 in aarc64 repo, installing... on Raspberry 3b
2021-09-18 Yay it runs:

### archlinuxarm
install aarch64:
https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3

on your raspi:

sudo useradd -m aaa
sudo passwd aaa

sudo usermod -aG dialout aaa
sudo usermod -aG users aaa
sudo usermod -aG tty aaa
sudo usermod -aG uucp aaa
sudo usermod -aG video aaa
sudo usermod -aG input aaa

copy files from Controller_Motion/software/raspberry to corresponding systemfolder

Install
- qt6-tools
- python-opengl
- qt6-svg
- python-pyserial-asyncio (from aur)

sudo systemctl enable getty@tty2
sudo systemctl enable moc


### Raspbian (! pyside6 not yet in repo ... waiting !)
1. prepare a micro-sd card with raspberry os
2. put an empty file 'ssh' to boot-partition, this enables ssh
3. Boot Raspberry pi 4
4. search for your rasp ip-address ie: nmap -sn 192.168.1.0/24
5. ssh pi@192.168.1.x (pass= raspberry) 
6. Configure user
	sudo useradd -m aaa
	sudo passwd aaa
	sudo usermod -aG dialout aaa
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
13. fix for raspi random hold
	Edit /etc/sysctl.conf
	  Append:
	    vm.dirty_background_ratio = 5
	    vm.dirty_ratio = 10
14. Clone repo
	sudo apt install git
	git clone git@github.com:ambisonics-audio-association/MotionControllerUI.git
15. Setup service
	sudo cp Ambijockey/Controller_Mixer/software/raspberry/config/etc/systemd/system/mic.service /etc/systemd/system/
	sudo systemctl start mic.service
	sudo systemctl enable mic.service
	  if 'systemctl enable mic.service' throws an error 'invalid argument'
	    cd /etc/systemd/system/multi-user.target.wants
	    sudo ln -s /etc/systemd/system/mic.service
16. Setup static ip-address
	sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bck
	sudo touch /etc/dhcpcd.conf
	Edit /etc/dhcpcd.conf
	  interface eth0
	  static ip_address=192.168.43.51/24
	  static routers=192.168.43.1
	  static domain_name_servers=192.168.43.1 8.8.8.8
15. sudo apt purge bluez pi-bluetooth





====OLD====
/usr/share/X11/xorg.conf.d/40-libinput.conf
-------------------------------------------
option "TransformationMatrix" "0 -1 1 1 0 0 0 0 1"

90° = Option "TransformationMatrix" "0 -1 1 1 0 0 0 0 1"
180° = Option "TransformationMatrix" "-1 0 1 0 -1 1 0 0 1"
270° = Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"

.kivy/config.ini
----------------
hid_%(name)s = probesysfs, provider=hidinput,param=rotation=90,param=invert_x=1

/boot/config.txt
----------------
display_rotate=1
dtoverlay=pi3-disable-bt
	
pip3 install kivy