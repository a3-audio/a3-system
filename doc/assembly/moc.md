# A³ Motion Assembly
## PCB
### Mainboard
![[a3motion-schematic.jpg]]
![[a3motion-pcb-design.jpg]]
### Buttonmatrix
![[a3motion-buttons-schematic.jpg]]
![[a3motion-buttons-pcb-design.jpg]]

## Hardware

- runs on a Raspberry Pi 3 Model B
- powered with PoE -> downstep to 3v on Teensy
- sbc is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 1 multiplexer hc4051 (8ch)
        function: width and 3d-boost per channel
    - 2 hc4051
        function: Buttonmatrix
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 16 x status leds buttonmatrix
  