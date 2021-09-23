# A³ Mix Assembly
## PCB
Mainboard-pcb kicad project is in the hardware-section of Ambijockey Repo. It is ready to fabricate.

## Hardware
- Raspberry 3b
- Teensy 4.1
- PoE to 5V Adapter
- Raspberry and Teensy are connected via usb (/dev/ttyACM0)

- 4 multiplexer hc4051 (8ch each)
        function: audiochannel-control
        potis
        - gain 
        - eq hi
        - eq mid
        - eq low
        - volume
        mode-buttons
        - 3d on/off
        - fx on/off
    - 1 hc4051
        function: masterchannel-control
        potis
        - master volume
        - booth volume
        - phones mix
        - headphones volume
    - 5 led-buttons for heapdphones prelisten function (pfl)
    - 1 NeoPixel-strip (ws2811) 9 leds input vu
	- 1 NeoPixel-strip (ws2811) for fx and 3d-section
    - 8x32 led-matrix for output-vu