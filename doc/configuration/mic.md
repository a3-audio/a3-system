# A³ Mix Configuration
## Teensy
software/teensy/src/main.cpp << [[flashTeensy]]

## Raspberry Pi 3 Model B
[Install Raspbian](https://www.raspberrypi.org/documentation/computers/getting-started.html)

1. put an empty file 'ssh' on Raspbian boot-partition, this enables ssh
2. search for your Raspberry ip-address ie: nmap -sn 192.168.1.0/24
3. ssh pi@192.168.1.x (pass= raspberry) 

### Root operations on the Raspberry: 
```
apt update
apt upgrade

useradd -m aaa
passwd aaa

usermod -aG dialout aaa
usermod -aG users aaa
usermod -aG tty aaa
usermod -aG uucp aaa
```
#### Install depencies
```
apt install python python-osc python-pip git python3-numpy

pip install numpy process pyserial python-osc rpi_ws281x adafruit-circuitpython-neopixel --force-reinstall adafruit-blinka

apt purge bluez pi-bluetooth

exit

ssh aaa@192.168.1.x
userdel pi

```
#### Clone repository:
```
cd /home/aaa
git clone git@github.com:ambisonics-audio-association/Ambijockey.git
```
#### Copy files to corresponding system-folder:
```
ControllerMixer/software/raspberry
   └── config
       └── etc
           ├── dhcpcd.conf
           └── systemd
               └── system
                   └── mic.service
```
#### Configure the Raspberry:
``` 
raspi-config
	3 Interface Options > P8 Remote GPIO > yes

nano /boot/config.txt
	max_usb_current=1

nano /boot/cmdline.txt
	logo.nologo (to the end of line)

nano .bashrc
	export PATH="/home/aaa/.local/bin:$PATH"

``` 
#### Setup service:
``` 
systemctl start mic.service
systemctl enable mic.service
  if 'systemctl enable mic.service' throws an error 'invalid argument'
    cd /etc/systemd/system/multi-user.target.wants
    sudo ln -s /etc/systemd/system/mic.service
``` 
#### Setup static ip-address
``` 
mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bck
touch /etc/dhcpcd.conf
Edit /etc/dhcpcd.conf
  interface eth0
  static ip_address=192.168.43.51/24
  static routers=192.168.43.1
  static domain_name_servers=192.168.43.1 8.8.8.8
```
#### Not sure if we still need "fix for Raspberry random hold":
```
nano /etc/sysctl.conf
    vm.dirty_background_ratio = 5
    vm.dirty_ratio = 10
```