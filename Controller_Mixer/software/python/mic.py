# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
#!/usr/bin/python

import sys
import math
import time
import argparse
import serial  # pySerial https://pyserial.readthedocs.io/
import numpy as np

import board
import neopixel

from multiprocessing import Process

from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_server
from pythonosc import dispatcher

from typing import List, Any

pixel_pin = board.D10
num_pixels = 12

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False
)

def pixel_color(r,g,b):
    pixels.fill((r,g,b))
    pixels.show()

fx_state = np.zeros(10)

# OSC-Clients
osc_router = SimpleUDPClient('192.168.43.50', 9000)

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

#    print("peak: " + str(peak_db) + " " + str(peak_index))
#    print("rms: " + str(rms_db) + " " + str(rms_index))

    sendData("VU" + vu + "," + str(peak_index) + "," + str(rms_index))

def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[2]

    peak = osc_arguments[0]
    rms = osc_arguments[1]

    # clamp to above 0 to avoid numerical error
    if peak == 0.0:
        peak = sys.float_info.epsilon
    if rms == 0.0:
        rms = sys.float_info.epsilon

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
                sendData("L1,")
                print("B1")
            if track == "2":
                osc_router.send_message("/ambijockey/mic/ch/2/pfl/", value)
                sendData("L2,")
                print("B2")
            if track == "3":
                osc_router.send_message("/ambijockey/mic/ch/3/pfl/", value)
                sendData("L3,")
                print("B3")
            if track == "4":
                osc_router.send_message("/ambijockey/mic/ch/4/pfl/", value)
                sendData("L4,")
                print("B4")
            if track == "5":
                osc_router.send_message("/ambijockey/mic/ch/master/pfl/", value)
                sendData("L5,")
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
                if potNr == "6":
                    if float(value) > 0.7 and fx_state[0]==0:
                        fx_state[0] = 1
                        pixels[5] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/1/fx/", 1)
                    elif float(value) > 0.7 and fx_state[0]==1:
                        fx_state[0] = 0
                        pixels[5] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/1/fx/", 0)
                if potNr == "7":
                    if float(value) > 0.7 and fx_state[1]==0:
                        fx_state[1] = 1
                        pixels[4] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/2/fx/", 1)
                    elif float(value) > 0.7 and fx_state[1]==1:
                        fx_state[1] = 0
                        pixels[4] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/2/fx/", 0)
                if potNr == "8":
                    if float(value) > 0.7 and fx_state[2]==0:
                        fx_state[2] = 1
                        pixels[3] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/3/fx/", 1)
                    elif float(value) > 0.7 and fx_state[2]==1:
                        fx_state[2] = 0
                        pixels[3] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/3/fx/", 0)
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
                if potNr == "6":
                    if float(value) > 0.7 and fx_state[3]==0:
                        fx_state[3] = 1
                        pixels[2] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/4/fx/", 1)
                    elif float(value) > 0.7 and fx_state[3]==1:
                        fx_state[3] = 0
                        pixels[2] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/4/fx/", 0)
                if potNr == "7":
                    if float(value) > 0.7 and fx_state[4]==0:
                        fx_state[4] = 1
                        pixels[6] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/1/3d/", 1)
                    elif float(value) > 0.7 and fx_state[4]==1:
                        fx_state[4] = 0
                        pixels[6] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/1/3d/", 0)
                if potNr == "8":
                    if float(value) > 0.7 and fx_state[5]==0:
                        fx_state[5] = 1
                        pixels[7] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/2/3d/", 1)
                    elif float(value) > 0.7 and fx_state[5]==1:
                        fx_state[5] = 0
                        pixels[7] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/2/3d/", 0)
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
                if potNr == "6":
                    if float(value) > 0.7 and fx_state[6]==0:
                        fx_state[6] = 1
                        pixels[8] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/3/3d/", 1)
                    elif float(value) > 0.7 and fx_state[6]==1:
                        fx_state[6] = 0
                        pixels[8] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/3/3d/", 0)
                if potNr == "7":
                    if float(value) > 0.7 and fx_state[7]==0:
                        fx_state[7] = 1
                        pixels[9] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/4/3d/", 1)
                    elif float(value) > 0.7 and fx_state[7]==1:
                        fx_state[7] = 0
                        pixels[9] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/4/3d/", 0)
                if potNr == "8":
                    if float(value) > 0.7 and fx_state[8]==0:
                        fx_state[8] = 1
                        pixels[0] = (255,0,0)
                        pixels[11] = (0,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/fxmode/hipass", 1)
                        osc_router.send_message("/ambijockey/mic/ch/fxmode/lopass", 0)
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
                if potNr == "6":
                    if float(value) > 0.7 and fx_state[8]==1:
                        fx_state[8] = 0
                        pixels[0] = (0,0,0)
                        pixels[11] = (255,0,0)
                        pixels.show()
                        osc_router.send_message("/ambijockey/mic/ch/fxmode/hipass", 0)
                        osc_router.send_message("/ambijockey/mic/ch/fxmode/lopass", 1)
                if potNr == "7":
                    osc_router.send_message("/ambijockey/mic/ch/fxparm/fxfreq", value)
                    print("T" + track + " P" + potNr + " " + value)
                if potNr == "8":
                    osc_router.send_message("/ambijockey/mic/ch/fxparm/fxres", value)
                    print("T" + track + " P" + potNr + " " + value)
            if track == "5":
                if potNr == "1":
                    osc_router.send_message("/ambijockey/mic/ch/master/volume/", value)
                    print("T" + track + " P" + potNr + " " + value)
                if potNr == "2":
                    osc_router.send_message("/ambijockey/mic/ch/master/booth/", value)
                    print("T" + track + " P" + potNr + " " + value)
                if potNr == "3":
                    osc_router.send_message("/ambijockey/mic/ch/master/phMix/", value)
                    print("T" + track + " P" + potNr + " " + value)
                if potNr == "4":
                    osc_router.send_message("/ambijockey/mic/ch/master/phVol/", value)
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
