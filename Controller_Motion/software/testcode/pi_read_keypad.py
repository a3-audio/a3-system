#!/usr/bin/python3
"""
Read out the Keypad

the key are conect to the pi with a 74CH4051
s0 ----- GPIO_22
s1 ----- GPIO_27
s2 ----- GPIO_17
MUX1_z--- GPIO_04
MUX2_z--- GPIO_05

"""
import RPi.GPIO as gpio
import numpy as np
from time import sleep

# var
s0 = 22
s1 = 27
s2 = 17
mux1 = 4  # z
mux2 = 5  # z
mux1_out = [0, 1, 2, 3, 4, 5, 6, 7]

gpio.setmode(gpio.BCM)

# setup PIN's
gpio.setup(s0, gpio.OUT)
gpio.setup(s1, gpio.OUT)
gpio.setup(s2, gpio.OUT)
gpio.setup(mux1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(mux2, gpio.IN, pull_up_down=gpio.PUD_DOWN)


def read_mux_pin(z, pin):
    """
    docstring
    """
    bit_addr = np.binary_repr(pin, width=3)
    gpio.output(s0, int(bit_addr[0]))
    gpio.output(s1, int(bit_addr[1]))
    gpio.output(s2, int(bit_addr[2]))
    return gpio.input(z)


if __name__ == "__main__":
    try:
        while True:
            for i in range(8):
                mux1_out[i] = read_mux_pin(mux1, i)
            print(mux1_out)
        sleep(1/35)
    except KeyboardInterrupt:
        gpio.cleanup()
