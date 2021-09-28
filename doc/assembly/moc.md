# A³ Motion Assembly
## PCB
A³ Motion
### Mainboard
### Buttonmatrix
## Hardware
- runs on a raspberry 3b
- powered with PoE -> downstep to 3v on Teensy
- sbc is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 1 multiplexer hc4051 (8ch)
        function: width and 3d-boost per channel
    - 2 hc4051
        function: Buttonmatrix
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 16 x status leds buttonmatrix