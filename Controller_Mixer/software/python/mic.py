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

import math
import time
import argparse
import serial  # pySerial https://pyserial.readthedocs.io/
import numpy as np

from multiprocessing import Process

from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
from pythonosc import dispatcher

from typing import List, Any

# OSC-Clients
osc_router = SimpleUDPClient('192.168.43.50', 9001)

# OSC-Server
osc_vu_receive_port = 7771

vu_channel_to_led_count = {
    "01" : 9,
    "02" : 9,
    "03" : 9,
    "04" : 9,
    "05" : 32,
    "06" : 32,
    "07" : 32,
    "08" : 32,
    "09" : 32,
    "10" : 32,
    "11" : 32,
    "12" : 32,
}

def db_value_to_index(value: float, num_leds: int):
    index = int(np.interp(value, [-60, 0], [0, num_leds]))
    if index == num_leds:
        index = num_leds - 1
    return index

def send_vu_data(vu: str, peak_db: float, rms_db: float):
    num_leds = vu_channel_to_led_count[vu]
    peak_index = db_value_to_index(peak_db, num_leds)
    rms_index = db_value_to_index(rms_db, num_leds)

    print("peak: " + str(peak_db) + " " + str(peak_index))
    print("rms: " + str(rms_db) + " " + str(rms_index))

    sendData("VU" + vu + "," + str(peak_index) + "," + str(rms_index))

def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[2]

    # divide by two to match peak-to-peak scale with rms
    peak = osc_arguments[0] / 2
    rms = osc_arguments[1]

    peak_db = 20 * math.log(peak)
    rms_db  = 20 * math.log(rms)

    send_vu_data(vu, peak_db, rms_db)

# Serial communication
ser = serial.Serial('/dev/ttyACM0', 115200)
ser.flush()

def sendData(data): # send Serial data
    data += "\r\n"
    ser.write(data.encode())

def serial_handler(): # dispatch from serial strem and send to osc

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

if __name__ == '__main__':

    proc1 = Process(target=serial_handler)
    proc1.start()

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on for VU meter messages")
    parser.add_argument("--port", type=int,
                        default=osc_vu_receive_port, help="The port to listen on for VU meter messages")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/vu/*", vu_handler)
    
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
