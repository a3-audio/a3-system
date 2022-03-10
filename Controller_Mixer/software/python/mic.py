# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021-2022 Patric Schmitz, Raphael Eismann, Jendrik Bradaczek
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

pixel_pin = board.D18
num_pixels = 12

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False
)

pixel_fx_mode_highpass = 0
pixel_fx_mode_lowpass = 11

color_led_on = (255,0,0)
color_led_off = (0,0,0)

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

# channel strips 1-4
analog_pots_per_channel_to_osc_param = {
    "0": "gain",
    "1": "hi",
    "2": "mid",
    "3": "lo",
    "4": "volume",
}

# master section pots mapping
master_pots_to_osc_message = {
    "0": "/mic/channel/master/volume",
    "1": "/mic/channel/master/booth",
    "2": "/mic/channel/master/phMix",
    "3": "/mic/channel/master/phVol",
    "6": "/mic/channel/fxparm/fxfreq",
    "7": "/mic/channel/fxparm/fxres",
}

# fx and 3d mode button mapping
fx_3d_mode_buttons_to_osc_message = {
    "0": "/mic/channel/0/fx",
    "1": "/mic/channel/1/fx",
    "2": "/mic/channel/2/fx",
    "3": "/mic/channel/3/fx",
    "4": "/mic/channel/0/3d",
    "5": "/mic/channel/1/3d",
    "6": "/mic/channel/2/3d",
    "7": "/mic/channel/3/3d",
}


# fx ledstrip remapping
fx_and_mode_leds = [5,4,3,2,6,7,8,9]

time_last_receive = 0

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


def send_pfl_leds_data(track: str, pfl_led_on: int):
    message = "PFL" + str(track) + "," + str(pfl_led_on)
    sendData(message)
    print(message)

def pfl_led_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    print(f'pfl_led_handler: {address}')

    words = address.split("/")
    channel = words[2]

    pfl_led_on = int(osc_arguments[0])
    send_pfl_leds_data(channel, pfl_led_on)


# Serial communication
ser = serial.Serial('/dev/ttyACM0', 115200)
ser.flush()

def sendData(data): # send Serial data
    data += "\r\n"
    ser.write(data.encode())

def serial_handler(): # dispatch from serial stream and send to osc

    while True:
        line = ser.readline().decode('utf-8').rstrip()

        # global time_last_receive
        # current_time_ns = time.clock_gettime_ns(time.CLOCK_REALTIME)
        # delta_time_ms = (current_time_ns - time_last_receive)/1e6
        # if delta_time_ms < 10:
        #     continue
        # print(f'time delta: {delta_time_ms}')
        # time_last_receive = current_time_ns

        print(line)

        words = line.split(":")

        # # fx mode buttons
        # if words[0] == "FX_MODE":
        #     print("fx mode switch")
        #     high_pass = words[1] == "HIGH_PASS"

        #     pixels[pixel_fx_mode_highpass] = color_led_on if high_pass else color_led_off
        #     pixels[pixel_fx_mode_lowpass] = color_led_off if high_pass else color_led_on
        #     pixels.show()

        #     osc_router.send_message("/mic/channel/fxmode/hipass", 1 if high_pass else 0)
        #     osc_router.send_message("/mic/channel/fxmode/lopass", 0 if high_pass else 1)

        #     continue

        track = words[1]
        mode = words[2]
        index = words[3]
        value = words[4]

        # Buttons
        if mode == "B":
            osc_router.send_message("/mic/channel/" + track + "/pfl", value)
            print("B" + track)

        # Potis
        if mode == "P":
            # the 4 channel strips
            channel_names = map(str, range(4))
            if track in channel_names:
                if index in analog_pots_per_channel_to_osc_param:
                    osc_router.send_message("/mic/channel/" + track + "/" +
                                            analog_pots_per_channel_to_osc_param[index], value)

            # pots in the master section
            if track == "master":
                if index in master_pots_to_osc_message:
                    osc_router.send_message(master_pots_to_osc_message[index], value)

            # fx and 3d buttons
            if track == "fx":
                if index in fx_3d_mode_buttons_to_osc_message:
                    osc_router.send_message(fx_3d_mode_buttons_to_osc_message[index], value)


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
    dispatcher.map("/pfl_led/*", pfl_led_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
