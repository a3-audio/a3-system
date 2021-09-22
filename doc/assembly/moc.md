# A³ Motion Assembly
## PCB
### Mainboard
### Buttonmatrix
## Hardware
- powered with PoE -> downstep to 3V inside
- runs on a x86-sbc
- sbc is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 1 multiplexer hc4051 (8ch)
        function: width and 3d-boost per channel
    - 2 hc4051
        function: Buttonmatrix
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 16 x status leds buttonmatrix