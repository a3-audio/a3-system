# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Raphael Eismann, Jendrik Bradaczek 
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
    "1": "gain",
    "2": "hi",
    "3": "mid",
    "4": "lo",
    "5": "volume",
}

# master section pots
master_pots_to_osc_message = {
    "1": "/mic/channel/master/volume/",
    "2": "/mic/channel/master/booth/",
    "3": "/mic/channel/master/phMix/",
    "4": "/mic/channel/master/phVol/",
    "7": "/mic/channel/fxparm/fxfreq",
    "8": "/mic/channel/fxparm/fxres",
}

# fx_and_3d_mode_button_split
fx_and_3d_mode_name = {
    "1": "fx",
    "2": "3d",
}

# split multiplexer in two sections for fx mode and 3d mode buttons
fx_and_3d_mode_button_multiplexer_split = [1,2,3,4,1,2,3,4]

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


def send_pfl_leds_data(track: str, mute: float):
    message = "PFL" + str(track) + "," + str(mute)
    sendData(message)
    print(message)

def pfl_leds_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[2]

    mute = int(osc_arguments[0])
    send_pfl_leds_data(track, mute)


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

        words = line.split(":")

        # fx mode buttons
        if words[0] == "FX_MODE":
            print("fx mode switch")
            high_pass = words[1] == "HIGH_PASS"

            pixels[pixel_fx_mode_highpass] = color_led_on if high_pass else color_led_off
            pixels[pixel_fx_mode_lowpass] = color_led_off if high_pass else color_led_on
            pixels.show()

            osc_router.send_message("/mic/channel/fxmode/hipass", 1 if high_pass else 0)
            osc_router.send_message("/mic/channel/fxmode/lopass", 0 if high_pass else 1)

            continue

        track = words[1]
        mode = words[2]
        potNr = words[3]
        value = words[4]

        # Buttons
        if mode == "B":
            if track == "1":
                osc_router.send_message("/mic/channel/1/pfl/", value)
                print("B1")
            if track == "2":
                osc_router.send_message("/mic/channel/2/pfl/", value)
                print("B2")
            if track == "3":
                osc_router.send_message("/mic/channel/3/pfl/", value)
                print("B3")
            if track == "4":
                osc_router.send_message("/mic/channel/4/pfl/", value)
                print("B4")
            if track == "5":
                osc_router.send_message("/mic/channel/master/pfl/", value)
                print("B5")
        # Potis
        if mode == "P":
            track_nr = int(track)

            # the 4 channel strips
            if track_nr >= 1 and track_nr <= 4:
                if potNr in analog_pots_per_channel_to_osc_param:
                    osc_router.send_message("/mic/channel/" + str(track_nr) + "/" +
                                            analog_pots_per_channel_to_osc_param[potNr] + "/", value)

            # pots in the master section
            if track_nr == 5:
                if potNr in master_pots_to_osc_message:
                    osc_router.send_message(master_pots_to_osc_message[potNr], value)

            # fx and 3d buttons
            if track == "6":
                for i in range(8):
                    if potNr == str(i+1):
                        if int(value) and fx_state[i]==0:
                            fx_state[i] = 1
                            pixels[fx_and_mode_leds[i]] = (255,0,0)
                            pixels.show()
                            if i <= 3:
                                osc_router.send_message("/mic/channel/" + str(fx_and_3d_mode_button_multiplexer_split[i]) + "/fx/", value)
                            else:
                                osc_router.send_message("/mic/channel/" + str(fx_and_3d_mode_button_multiplexer_split[i]) + "/3d/", value)
                        elif int(value) and fx_state[i]==1:
                            fx_state[i] = 0
                            pixels[fx_and_mode_leds[i]] = (0,0,0)
                            pixels.show()
                            if i <= 3:
                                osc_router.send_message("/mic/channel/" + str(fx_and_3d_mode_button_multiplexer_split[i]) + "/fx/", value)
                            else:
                                osc_router.send_message("/mic/channel/" + str(fx_and_3d_mode_button_multiplexer_split[i]) + "/3d/", value)


# " str(fx_and_3d_mode_name) "

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
    dispatcher.map("/mute/*", pfl_leds_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
