# Ambijocky Server README

## Static IP-Addresses
aaa 192.168.43.50 (server)
mic 192.168.43.51 (mixer controller)
moc 192.168.43.52 (motion controller)

## Dependences

sudo pacman -S python3
sudo pacman -S python-osc

pip install numpy
pip install pyserial

## Configuration

sudo chmod a+rw /dev/ttyACM0
stat /dev/ttyACM0stat

cp /etc/dhcpcd.conf /etc/dhcpcd-bck.conf
cp config/etc/dhcpcd.conf /etc/dhcpcd.conf
