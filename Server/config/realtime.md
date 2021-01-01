REALTIME PRIORITY CONFIGURATION

In Audiolinux realtime priority is assigned by 2 services: rtirq for irq priority and rtapp for application priority.

1) RTIRQ configuration

The default configuration file is /etc/rtirq.conf
The important section is this one
RTIRQ_NAME_LIST="xhci"
In the default configuration it will give the defined priority to xhci usb devices.
To check the realtime priorities you can use rtstatus.  If you change xhci to usb in rtirq.conf you will see something like this:

[audiolinux@archlinux ~]$ rtstatus
REALTIME PRIORITY
IRQS
RTPRIO COMMAND
    90 irq/20-ehci_hcd
    90 irq/25-xhci_hcd
    89 irq/23-ehci_hcd
    50 irq/9-acpi
    50 irq/8-rtc0
    50 irq/24-nvidia
    50 irq/26-ahci[000
    50 irq/27-mei_me
    50 irq/5-parport0
    50 irq/18-i801_smb
    50 irq/17-snd_hda_
    50 irq/28-enp4s0
    49 irq/24-s-nvidia

As you can see we have here multiple devices at irq 20, 23 and 25 with high priority, but only one is connected to the DAC.
To know the irq of your DAC, you can type rtcards. In this example:

USB INTERRUPTS AND DEVICES

USB1 IRQ=20 EHCI Host Controller
USB2 IRQ=25 a096, c077, HP Color LaserJet Pro M252dw, Logitech USB Optical Mouse, SA9023 USB Audio, USB Keyboard, USB Keyboard Consumer Control, USB Keyboard Keyboard, USB Keyboard System Control, USB Optical Mouse, xHCI Host Controller
USB3 IRQ=23 EHCI Host Controller
USB4 IRQ=25 Elements 25A1, xHCI Host Controller

In this case the DAC (SA9023 USB Audio) is at irq 25, more specifically irq/25-xhci_hcd. Because of this we will change the rtirq.conf line from
RTIRQ_NAME_LIST="usb"
to
RTIRQ_NAME_LIST="xhci"
This way the max. priority specified in the configuration file will be given only to the DAC.

NETWORK BRIDGE
If you are using your computer as a server for a second remote computer as NAA, the DAC will not be attached to the the first. It could be a good idea to give high priority to the network interface. In our example:
RTIRQ_NAME_LIST="enp4s0"
In case of a NETWORK BRIDGE you will use the interface connected to the NAA, not the one connected to internet network.
In the second computer (NAA) you can use the previous configuration
RTIRQ_NAME_LIST="xhci"

2) RTAPP configuration

Please read first the readme at /usr/share/doc/rtapp/readme.txt

The default configuration file is /etc/rtapp/rtapp.conf

APPLICATIONS="mpd hqplayer hqplayerd squeezelite networkaudiod RoonBridge RoonAppliance sox mediacenter25 spotifyd"

MAX_PRIORITY="85"

MODE="autodec"

In general you don't need to modify the list of applications, but if you are using Roon as control point for HQPlayer, the real player would be the last one, so we suggest to remove RoonAppliance from that list. This is true in general if you are using one of the applications in the list only as a control point.

You can add a new application to the list, if you want to give realtime priority.
