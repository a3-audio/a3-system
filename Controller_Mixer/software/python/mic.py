#!/usr/bin/python

""" AAA-MIX, mic.py
- powered with PoE -> downstep to 3V inside
- runs on raspberry pi 3b
- raspberry is connected via usb (/dev/ttyACM0) to
- teensy 4.1, it has
    - 4 multiplexer hc4051 (8ch each)
        function: audiochannel-control
        potis
        - gain 
        - eq hi
        - eq mid
        - eq low
        - volume
        mode-buttons
        - mono
        - stereo
        - ambionic
    - 1 hc4051
        function: masterchannel-control
        potis
        - master-volume
        - booth-volume
        - phones mix
        - no headphone volume here!?:
            we feed line-level to builtin headphone-amplifier and control it analog
    - 5 led-buttons for heapdphones prelisten function (pfl)
    - 1 NeoPixel-strip (ws2811 led-controller)
        - 3 leds mode-status
        - 9 leds input vu
    - 9 mode-buttons, 3 per channel
        - mono
        - stereo
        - 3d
    - 1 8x32 led-matrix for output-vu
- Open Sound Control (osc)
    - receives osc messages from 
        - aaa-core/vu-meter.scd 
        - function: vu-meters
    - sends osc messages to 
        - aaa-core/server.py
        - function: daw-controller, 4ch dj-mixer style

"""

import serial  # pySerial https://pyserial.readthedocs.io/
import numpy
import time
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
from typing import List, Any
from pythonosc import dispatcher
import argparse
import threading

# OSC-Clients
osc_router = SimpleUDPClient('192.168.43.50', 9001)

# OSC-Server
oscRouterPort = 7771

def sendData(data):
    data += "\r\n"
    ser.write(data.encode())

def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[2]

    peak = osc_arguments[0]
    rms = osc_arguments[1]
#    print(str(peak) + " - " + str(rms))

    if vu == "1":
        sendData("VU01," + str(peak) + "," + str(rms))
        print("VU01," + str(peak) + "," + str(rms))
    if vu == "2":
        sendData("VU02," + str(peak) + "," + str(rms))
    if vu == "3":
        sendData("VU03," + str(peak) + "," + str(rms))
    if vu == "4":
        sendData("VU04," + str(peak) + "," + str(rms))

# def button_handler(data): TODO

if __name__ == '__main__':


    def serialThread():    
        ser = serial.Serial('/dev/ttyACM0', 115200)
        ser.flush()
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()

                words = line.split(":")
                track = words[1]
                mode = words[2]
                potNr = words[3]
                value = words[4]


              # Buttons
                if mode == "B":
                    if track == "1":
                        osc_router.send_message("/ambijockey/mic/ch/1/pfl/", value)
                        sendData("L1")
                        print("B1")
                    if track == "2":
                        osc_router.send_message("/ambijockey/mic/ch/2/pfl/", value)
                        sendData("L2")
                        print("B2")
                    if track == "3":
                        osc_router.send_message("/ambijockey/mic/ch/3/pfl/", value)
                        sendData("L3")
                        print("B3")
                    if track == "4":
                        osc_router.send_message("/ambijockey/mic/ch/4/pfl/", value)
                        sendData("L4")
                        print("B4")
                    if track == "5":
                        osc_router.send_message("/ambijockey/mic/ch/master/pfl/", value)
                        sendData("L5")
                        print("B5")
              # Potis
                if mode == "P":
                    if track == "1":
                        if potNr == "1":
                            osc_router.send_message("/ambijockey/mic/ch/1/gain/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "2":
                            osc_router.send_message("/ambijockey/mic/ch/1/hi/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "3":
                            osc_router.send_message("/ambijockey/mic/ch/1/mid/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "4":
                            osc_router.send_message("/ambijockey/mic/ch/1/lo/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "5":
                            osc_router.send_message("/ambijockey/mic/ch/1/volume/", value)
                            print("T" + track + " P" + potNr + " " + value)
                    if track == "2":
                        if potNr == "1":
                            osc_router.send_message("/ambijockey/mic/ch/2/gain/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "2":
                            osc_router.send_message("/ambijockey/mic/ch/2/hi/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "3":
                            osc_router.send_message("/ambijockey/mic/ch/2/mid/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "4":
                            osc_router.send_message("/ambijockey/mic/ch/2/lo/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "5":
                            osc_router.send_message("/ambijockey/mic/ch/2/volume/", value)
                            print("T" + track + " P" + potNr + " " + value)
                    if track == "3":
                        if potNr == "1":
                            osc_router.send_message("/ambijockey/mic/ch/3/gain/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "2":
                            osc_router.send_message("/ambijockey/mic/ch/3/hi/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "3":
                            osc_router.send_message("/ambijockey/mic/ch/3/mid/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "4":
                            osc_router.send_message("/ambijockey/mic/ch/3/lo/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "5":
                            osc_router.send_message("/ambijockey/mic/ch/3/volume/", value)
                            print("T" + track + " P" + potNr + " " + value)
                    if track == "4":
                        if potNr == "1":
                            osc_router.send_message("/ambijockey/mic/ch/4/gain/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "2":
                            osc_router.send_message("/ambijockey/mic/ch/4/hi/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "3":
                            osc_router.send_message("/ambijockey/mic/ch/4/mid/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "4":
                            osc_router.send_message("/ambijockey/mic/ch/4/lo/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "5":
                            osc_router.send_message("/ambijockey/mic/ch/4/volume/", value)
                            print("T" + track + " P" + potNr + " " + value)
                    if track == "5":
                        if potNr == "1":
                            osc_router.send_message("/ambijockey/mic/ch/master/volume/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "2":
                            osc_router.send_message("/ambijockey/mic/ch/master/hi/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "3":
                            osc_router.send_message("/ambijockey/mic/ch/master/mid/", value)
                            print("T" + track + " P" + potNr + " " + value)
                        if potNr == "4":
                            osc_router.send_message("/ambijockey/mic/ch/master/lo/", value)
                            print("T" + track + " P" + potNr + " " + value)

    def oscThread():
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
        parser.add_argument("--port", type=int,
                            default=oscRouterPort, help="The port to listen on")
        args = parser.parse_args()

        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/vu/*", vu_handler)
        
        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
        time.sleep(0.001)

    t1 = threading.Thread(target=oscThread())
    t2 = threading.Thread(target=serialThread())

    t1.start()
    t2.start()

