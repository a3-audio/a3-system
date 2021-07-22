"""
this version is just a steady hardcoded version of osc-router. It will
transform into more dynamic code with external configfiles for osc in-
and output mappings.
For now it takes OSC-Adresses, interpolates values and sends them to
destinations:
"""

import argparse
import math
import numpy
import re
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

# OSC-Server
oscRouterPort = 9000

# OSC-Clients
ctrl_mixer = SimpleUDPClient('192.168.43.51', 8500)  # Set IP Adress
ctrl_motion = SimpleUDPClient('192.168.43.52', 8700)  # Set IP Adress
reaper = SimpleUDPClient('127.0.0.1', 9001)
non_mixer = SimpleUDPClient('127.0.0.1', 9002)
iem_1 = SimpleUDPClient('127.0.0.1', 1337)
iem_2 = SimpleUDPClient('127.0.0.1', 1338)
iem_3 = SimpleUDPClient('127.0.0.1', 1339)
iem_4 = SimpleUDPClient('127.0.0.1', 1340)

# reaper channelnumbers
masterbus = "6"  # mastervolume is controlled by /master/volume
dj1_cb = "26"  # cb = channelbus
dj1_in = "27"  # in = input
dj2_cb = "35"
dj2_in = "36"
dj3_cb = "44"
dj3_in = "45"
dj4_cb = "53"
dj4_in = "54"
dj1_pfl = "18"
dj2_pfl = "19"
dj3_pfl = "20"
dj4_pfl = "21"
mainmixbus = "22"


def ctrlMotionToIem_handler(address: str,
                            *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[4]
    param = words[5]

    # print(words)
    #value = osc_arguments
    #print("/ctrlMotion/track/" + track + "/" + param + "/ : " + str(value))

    if track == "1":
        if param == "xyz":
            iem_1.send_message("/CoordinateConverter/xPos",
                               numpy.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_1.send_message("/CoordinateConverter/yPos",
                               numpy.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_1.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_1.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "reverb":
            reaper.send_message("/track/" + dj1_in + "/fx/2/fxparam/1/value", osc_arguments[0])

    if track == "2":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_2.send_message("/CoordinateConverter/xPos",
                               numpy.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_2.send_message("/CoordinateConverter/yPos",
                               numpy.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_2.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_2.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "reverb":
            reaper.send_message("/track/" + dj2_in + "/fx/2/fxparam/1/value", osc_arguments[0])

    if track == "3":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_3.send_message("/CoordinateConverter/xPos",
                               numpy.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_3.send_message("/CoordinateConverter/yPos",
                               numpy.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_3.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_3.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "reverb":
            reaper.send_message("/track/" + dj3_in + "/fx/2/fxparam/1/value", osc_arguments[0])

    if track == "4":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_4.send_message("/CoordinateConverter/xPos",
                               numpy.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_4.send_message("/CoordinateConverter/yPos",
                               numpy.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_4.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_4.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "reverb":
            reaper.send_message("/track/" + dj4_in + "/fx/2/fxparam/1/value", osc_arguments[0])


val_send_ch1_xyz = [0, 0, 0]
val_send_ch2_xyz = [0, 0, 0]
val_send_ch3_xyz = [0, 0, 0]
val_send_ch4_xyz = [0, 0, 0]


def iemToCtrlMotion_handler(address: str,
                            *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[2]
    param = words[3]

    print(words)
    #value = osc_arguments[0]
    #print("/CoordinateConverter/" + track + "/" + param + " : " + str(value))

    if track == "1":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch1_xyz[1] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch1_xyz[0] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch1_xyz[2] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/ambiJocky/motion/ch/1/pos/xyz", val_send_ch1_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/1/width", osc_arguments[0])

    if track == "2":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch2_xyz[1] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch2_xyz[0] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch2_xyz[2] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/ambiJocky/motion/ch/2/pos/xyz", val_send_ch2_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/2/width", osc_arguments[0])

    if track == "3":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch3_xyz[1] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch3_xyz[0] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch3_xyz[2] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/ambiJocky/motion/ch/3/pos/xyz", val_send_ch3_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/3/width", osc_arguments[0])

    if track == "4":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch4_xyz[1] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch4_xyz[0] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch4_xyz[2] = (numpy.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/ambiJocky/motion/ch/4/pos/xyz", val_send_ch4_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/4/width", osc_arguments[0])


class CH_handler(object):
    """
    Hier mit werden die eingehenden OSC-Messages auf die Server funtionen gemappt
    """

    def __init__(self):
        pass

    def msg_in(self, address: str, *osc_args: List[Any]) -> None:
        """
        docstring
        """
        words = address.split("/")
        ch = words[2]
        ch_nr = int(ch[len(ch)-1])
        contoler = words[3]
        ctr_function = []
        for i in range(4, len(words)):
            ctr_function.append(words[i])

        # Motion-Controller
        if contoler == "motion":
            if ctr_function[0] == "reset":
                pass
            elif ctr_function[0] == "pos":
                if ctr_function[1] == "cartesian":
                    print(osc_args)
                elif ctr_function[1] == "polar":
                    pass
            elif ctr_function[0] == "pos_x":
                pass
            elif ctr_function[0] == "pos_y":
                pass
            elif ctr_function[0] == "pos_r":
                pass
            elif ctr_function[0] == "pos_t":
                pass

def poti_handler(address: str,
                 *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[4]
    poti = words[5]

    value = osc_arguments[0]
    print(track + "." + poti + " : " + str(value))

    if track == "1":
        if poti == "gain":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj1/Gain/Gain%20(dB)", float(val))
            #xp = [0, 0.01,  0.3,  0.4,   0.5,  0.6,   0.7,  0.8,   0.9,  1.0]
            #fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48,  0.485, 0.49,  0.495, 0.5]
            #val = numpy.interp(value, xp, fp)
            #reaper.send_message("/track/" + dj1_in + "/gain", val)
        if poti == "hi":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj1/DJ%20EQ/Hi%20gain%20(dB)", float(val))
            #val = numpy.interp(value, [0, 1], [0.05, 0.50])
            #reaper.send_message("/track/" + dj1_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj1/DJ%20EQ/Mid%20gain%20(dB)", float(val))
            #val = numpy.interp(value, [0, 1], [0.01, 0.50])
            #reaper.send_message("/track/" + dj1_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj1/DJ%20EQ/Lo%20gain%20(dB)", float(val))
            #val = numpy.interp(value, [0, 1], [0.01, 0.50])
            #reaper.send_message("/track/" + dj1_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj1_cb + "/volume", val)
        if poti == "fx":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj1/Gain.1/Mute", float(value))
            non_mixer.send_message("/strip/dj1/Aux%20(A)/Gain%20(dB)", float(val))
            non_mixer.send_message("/strip/dj1/Aux%20(B)/Gain%20(dB)", float(val))
    elif track == "2":
        if poti == "gain":
            xp = [0, 0.01,  0.3,  0.4,   0.5,  0.6,   0.7,  0.8,   0.9,  1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48,  0.485, 0.49,  0.495, 0.5]
            val = numpy.interp(value, xp, fp)
            reaper.send_message("/track/" + dj2_in + "/gain", val)
        if poti == "hi":
            val = numpy.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj2_cb + "/volume", val)
        if poti == "fx":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj2/Gain.1/Mute", float(1 - value))
            non_mixer.send_message("/strip/dj2/Aux%20(A)/Gain%20(dB)", float(val))
            non_mixer.send_message("/strip/dj2/Aux%20(B)/Gain%20(dB)", float(val))
    elif track == "3":
        if poti == "gain":
            xp = [0, 0.01,  0.3,  0.4,   0.5,  0.6,   0.7,  0.8,   0.9,  1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48,  0.485, 0.49,  0.495, 0.5]
            val = numpy.interp(value, xp, fp)
            reaper.send_message("/track/" + dj3_in + "/gain", val)
        if poti == "hi":
            val = numpy.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj3_cb + "/volume", val)
        if poti == "fx":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj3/Gain.1/Mute", float(1 - value))
            non_mixer.send_message("/strip/dj3/Aux%20(A)/Gain%20(dB)", float(val))
            non_mixer.send_message("/strip/dj3/Aux%20(B)/Gain%20(dB)", float(val))
    elif track == "4":
        if poti == "gain":
            xp = [0, 0.01,  0.3,  0.4,   0.5,  0.6,   0.7,  0.8,   0.9,  1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48,  0.485, 0.49,  0.495, 0.5]
            val = numpy.interp(value, xp, fp)
            reaper.send_message("/track/" + dj4_in + "/gain", val)
        if poti == "hi":
            val = numpy.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = numpy.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj4_cb + "/volume", val)
        if poti == "fx":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj4/Gain.1/Mute", float(1 - value))
            non_mixer.send_message("/strip/dj4/Aux%20(A)/Gain%20(dB)", float(val))
            non_mixer.send_message("/strip/dj4/Aux%20(B)/Gain%20(dB)", float(val))
        if poti == "fxfreq":
            val = numpy.interp(value, [0, 1], [0, 0.921])
            non_mixer.send_message("/strip/dj4hipass/Glame%20Highpass%20Filter/Cutoff%20Frequency", float(value))
    elif track == "master":
        if poti == "volume":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + masterbus + "/volume", val)
        if poti == "booth":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/1/volume", val)
        if poti == "phMix":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/22/volume", val)
            reaper.send_message("/track/21/volume", 1 - val)
            reaper.send_message("/track/20/volume", 1 - val)
            reaper.send_message("/track/19/volume", 1 - val)
            reaper.send_message("/track/18/volume", 1 - val)
        if poti == "phVol":
            val = numpy.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/14/volume", val)
    elif track == "fxmode":
        if poti == "lopass":
            non_mixer.send_message("/strip/dj1hipass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj2hipass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj3hipass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj4hipass/Gain/Mute", float(value))
        if poti == "hipass":
            non_mixer.send_message("/strip/dj1lopass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj2lopass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj3lopass/Gain/Mute", float(value))
            non_mixer.send_message("/strip/dj4lopass/Gain/Mute", float(value))

def button_handler(address: str,
                   *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    button = words[4]
    mode = words[5]

    value = osc_arguments[0]
    if mode == "pfl":
        if button == "1":
            reaper.send_message("/track/" + dj1_pfl + "/mute", 0)
            reaper.send_message("/track/" + dj2_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj3_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj4_pfl + "/mute", 1)
#            reaper.send_message("/track/" + mainmixbus + "/mute", 1)

        if button == "2":
            reaper.send_message("/track/" + dj1_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj2_pfl + "/mute", 0)
            reaper.send_message("/track/" + dj3_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj4_pfl + "/mute", 1)
#            reaper.send_message("/track/" + mainmixbus + "/mute", 1)

        if button == "3":
            reaper.send_message("/track/" + dj1_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj2_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj3_pfl + "/mute", 0)
            reaper.send_message("/track/" + dj4_pfl + "/mute", 1)
#            reaper.send_message("/track/" + mainmixbus + "/mute", 1)

        if button == "4":
            reaper.send_message("/track/" + dj1_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj2_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj3_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj4_pfl + "/mute", 0)
#            reaper.send_message("/track/" + mainmixbus + "/mute", 1)

        if button == "master":
            reaper.send_message("/track/" + dj1_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj2_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj3_pfl + "/mute", 1)
            reaper.send_message("/track/" + dj4_pfl + "/mute", 1)
#            reaper.send_message("/track/" + mainmixbus + "/mute", 0)


def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[3]

    value = osc_arguments[0]

    if vu == "1":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = numpy.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/1/vu", val)
        # print(str(value))
    if vu == "2":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = numpy.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/2/vu", val)
        # print(str(value))
    if vu == "3":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = numpy.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/3/vu", val)
        # print(str(value))
    if vu == "4":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = numpy.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/4/vu", val)
        # print(str(value))
    if vu == "5":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = numpy.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/5/vu", val)
        # print(str(value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int,
                        default=oscRouterPort, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)
    ch1 = CH_handler()

    # Mixer-Controller
    dispatcher.map("/ambijockey/mic/ch/*", poti_handler)
    dispatcher.map("/ambijockey/mic/ch/*", button_handler)
    dispatcher.map("/reaper/vu/*", vu_handler)

    # Motion-Controller
    # dispatcher.map("/CoordinateConverter/*", iemToCtrlMotion_handler)
    dispatcher.map("/ambiJocky/motion/ch/*", ctrlMotionToIem_handler)
    dispatcher.map("/ambijockey/moc/ch/*", ctrlMotionToIem_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
