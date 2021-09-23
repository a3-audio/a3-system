# A³ Motion Configuration
## teensy
software/teensy/src/main.cpp << [[flashTeensy]]

## Raspberry
install aarch64:
https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3

On raspi:
```
useradd -m aaa
passwd aaa

usermod -aG dialout aaa
usermod -aG users aaa
usermod -aG tty aaa
usermod -aG uucp aaa
usermod -aG video aaa
usermod -aG input aaa
```

Copy files from Controller_Motion/software/raspberry to corresponding systemfolder

Install depencies
``` 
pacman -S qt6-tools python-opengl qt6-svg git
python-pyserial-asyncio (from aur)
``` 

Clone repo to /home/aaa/
``` 
git clone git@github.com:ambisonics-audio-association/MotionControllerUI.git /home/aaa
``` 

enable services
``` 
sudo systemctl enable getty@tty2
sudo systemctl enable moc
``` 

Setup static ip-address
``` 
mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bck
touch /etc/dhcpcd.conf
nano /etc/dhcpcd.conf
	  interface eth0
	  static ip_address=192.168.43.51/24
	  static routers=192.168.43.1
	  static domain_name_servers=192.168.43.1 8.8.8.8
``` 

Edit /boot/config.txt
``` 
display_rotate=1
dtoverlay=pi3-disable-bt
``` 