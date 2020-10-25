#!/usr/bin/python3
import RPi.GPIO as gpio
import time
# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse


# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("192.168.43.129", 9000, "aclientname")

gpio.setmode(gpio.BCM)

matrix = [["1ch1","1ch2","1ch3", "1ch4"],
    ["2ch1", "2ch2", "2ch3", "2ch4"],
    ["3ch1", "3ch2", "3ch3", "3ch4"],
    ["4ch1", "4ch2", "4ch3", "4ch4"]]

#spalte = [4, 17, 27, 22]
#zeile = [5, 6, 13, 19]
spalte = [5, 6, 13, 19]
zeile = [4, 17, 27, 22]

for j in range(4):
    gpio.setup(spalte[j], gpio.OUT)
    gpio.output(spalte[j], 1)

for i in range(4):
    gpio.setup(zeile[i], gpio.IN, pull_up_down = gpio.PUD_UP)

def keypad_press():
    while True:
        for j in range(4):
            gpio.output(spalte[j], 0)
            for i in range(4):
                if gpio.input(zeile[i]) == 0:
                    benutzerEingabe = matrix[i][j]
                    while gpio.input(zeile[i]) == 0:

                        pass
                    return benutzerEingabe                  
            gpio.output(spalte[j], 1)
    return False

def keypad_release():
    while True:
        for j in range(4):
            gpio.output(spalte[j], 0)
            for i in range(4):
                if gpio.input(zeile[i]) == 1:
                    benutzerEingabe = matrix[i][j]
                    while gpio.input(zeile[i]) == 1:

                        pass
                    return benutzerEingabe                  
            gpio.output(spalte[j], 1)
    return False

try:
    while True:

        addr = "/Button/" + keypad_press()
        msg = oscbuildparse.OSCMessage(addr, ",i", [1])
        osc_send(msg, "aclientname")

        
        # if keypad_press() == "1ch2":
        #     print("1ch2")
        #     # Build a simple message and send it.
        #     msg = oscbuildparse.OSCMessage("/test/me", ",sif", ["button2", 1, 2])
        #     osc_send(msg, "aclientname")
        
        osc_process()
        time.sleep(0.1)

except KeyboardInterrupt:
    gpio.cleanup()
    osc_terminate()