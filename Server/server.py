"""
This version is a static hardcoded version of osc-router. It will
transform into more dynamic code with external configfiles for osc in-
and output mappings.  For now it takes OSC adresses, interpolates
values and sends them to destinations.
"""

import argparse
import numpy as np
import re

from typing import List, Any

from pythonosc import dispatcher  # type: ignore
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient  # type: ignore

# OSC server config
osc_router_port = 9000

# OSC clients
ctrl_mixer = SimpleUDPClient('192.168.43.51', 8500)
ctrl_motion = SimpleUDPClient('192.168.43.52', 8700)
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

fxmodeval = "0"
fxstate1: float = 0
fxstate2: float = 0
fxstate3: float = 0
fxstate4: float = 0


def sethipass() -> None:
    global fxmodeval
    if fxmodeval == "1":
        global fxstate1
        global fxstate2
        global fxstate3
        global fxstate4
        reaper.send_message("/track/" + dj1_in + "/fx/4/bypass", fxstate1)
        reaper.send_message("/track/" + dj2_in + "/fx/4/bypass", fxstate2)
        reaper.send_message("/track/" + dj3_in + "/fx/4/bypass", fxstate3)
        reaper.send_message("/track/" + dj4_in + "/fx/4/bypass", fxstate4)
        reaper.send_message("/track/" + dj1_in + "/fx/5/bypass", 0)
        reaper.send_message("/track/" + dj2_in + "/fx/5/bypass", 0)
        reaper.send_message("/track/" + dj3_in + "/fx/5/bypass", 0)
        reaper.send_message("/track/" + dj4_in + "/fx/5/bypass", 0)


def setlopass() -> None:
    global fxmodeval
    if fxmodeval == "0":
        global fxstate1
        global fxstate2
        global fxstate3
        global fxstate4
        reaper.send_message("/track/" + dj1_in + "/fx/5/bypass", fxstate1)
        reaper.send_message("/track/" + dj2_in + "/fx/5/bypass", fxstate2)
        reaper.send_message("/track/" + dj3_in + "/fx/5/bypass", fxstate3)
        reaper.send_message("/track/" + dj4_in + "/fx/5/bypass", fxstate4)
        reaper.send_message("/track/" + dj1_in + "/fx/4/bypass", 0)
        reaper.send_message("/track/" + dj2_in + "/fx/4/bypass", 0)
        reaper.send_message("/track/" + dj3_in + "/fx/4/bypass", 0)
        reaper.send_message("/track/" + dj4_in + "/fx/4/bypass", 0)


def ctrlMotionToIem_handler(address: str,
                            *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[3]
    param = words[4]

    # print(words)
    # value = osc_arguments
    # print("/ctrlMotion/track/" + track + "/" + param + "/ : " + str(value))

    if track == "1":
        if param == "xyz":
            iem_1.send_message("/CoordinateConverter/xPos",
                               np.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_1.send_message("/CoordinateConverter/yPos",
                               np.interp(osc_arguments[0], [0, 1], [1, -1]))

    if track == "2":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_2.send_message("/CoordinateConverter/xPos",
                               np.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_2.send_message("/CoordinateConverter/yPos",
                               np.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_2.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_2.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "side":
            reaper.send_message("/track/" + dj2_in + "/fx/2/fxparam/1/value",
                                osc_arguments[0])

    if track == "3":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_3.send_message("/CoordinateConverter/xPos",
                               np.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_3.send_message("/CoordinateConverter/yPos",
                               np.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_3.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_3.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "side":
            reaper.send_message("/track/" + dj3_in + "/fx/2/fxparam/1/value",
                                osc_arguments[0])

    if track == "4":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_4.send_message("/CoordinateConverter/xPos",
                               np.interp(osc_arguments[1], [0, 1], [-1, 1]))
            iem_4.send_message("/CoordinateConverter/yPos",
                               np.interp(osc_arguments[0], [0, 1], [1, -1]))
            # iem_4.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        if param == "width":
            iem_4.send_message("/CoordinateConverter/radius", osc_arguments[0])
        if param == "side":
            reaper.send_message("/track/" + dj4_in + "/fx/2/fxparam/1/value",
                                osc_arguments[0])


val_send_ch1_xyz = [0, 0, 0]
val_send_ch2_xyz = [0, 0, 0]
val_send_ch3_xyz = [0, 0, 0]
val_send_ch4_xyz = [0, 0, 0]


def iemToCtrlMotion_handler(address: str,
                            *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[1]
    param = words[2]

    print(words)
    # value = osc_arguments[0]
    # print("/CoordinateConverter/" + track + "/" + param + " : " + str(value))

    if track == "1":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch1_xyz[1] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch1_xyz[0] = (np.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch1_xyz[2] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/moc/channel/1/pos/xyz", val_send_ch1_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/1/width", osc_arguments[0])

    if track == "2":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch2_xyz[1] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch2_xyz[0] = (np.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch2_xyz[2] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/moc/channel/2/pos/xyz", val_send_ch2_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/2/width", osc_arguments[0])

    if track == "3":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch3_xyz[1] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch3_xyz[0] = (np.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch3_xyz[2] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/moc/channel/3/pos/xyz", val_send_ch3_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/3/width", osc_arguments[0])

    if track == "4":
        if (param == "xPos" or param == "yPos" or param == "yPos"):
            if param == "xPos":
                val_send_ch4_xyz[1] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            if param == "yPos":
                val_send_ch4_xyz[0] = (np.interp(
                    osc_arguments[0], [-1, 1], [1, 0]))
            else:
                val_send_ch4_xyz[2] = (np.interp(
                    osc_arguments[0], [-1, 1], [0, 1]))
            ctrl_motion.send_message(
                "/moc/channel/4/pos/xyz", val_send_ch4_xyz)

        if param == "radius":
            ctrl_motion.send_message(
                "/ctrlMotion/track/4/width", osc_arguments[0])


def poti_handler(address: str,
                 *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[3]
    poti = words[4]

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float
    print(track + "." + poti + " : " + str(value))

    if track == "1":
        if poti == "gain":
            xp = [0, 0.01, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48, 0.485, 0.49, 0.495, 0.5]
            val = np.interp(value, xp, fp)
            reaper.send_message("/track/" + dj1_in + "/gain", val)
        if poti == "hi":
            val = np.interp(value, [0, 1], [0.05, 0.50])
            reaper.send_message("/track/" + dj1_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj1_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj1_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj1_cb + "/volume", val)
        if poti == "fx":  # its the fx-button
            global fxstate1
            fxstate1 = value
            sethipass()
            setlopass()
        if poti == "3d":
            reaper.send_message("/track/33/mute", value)
            reaper.send_message("/track/34/mute", 1 - value)
        if poti == "width":
            val = np.interp(value, [0, 1], [0, 1])
            iem_1.send_message("/StereoEncoder/width", float(val))
            # print(str(value))
        if poti == "side":
            reaper.send_message("/track/" + dj1_in + "/fx/2/fxparam/1/value",
                                value)
    elif track == "2":
        if poti == "gain":
            xp = [0, 0.01, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48, 0.485, 0.49, 0.495, 0.5]
            val = np.interp(value, xp, fp)
            reaper.send_message("/track/" + dj2_in + "/gain", val)
        if poti == "hi":
            val = np.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj2_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj2_cb + "/volume", val)
        if poti == "fx":
            global fxstate2
            fxstate2 = value
            sethipass()
            setlopass()
        if poti == "3d":
            reaper.send_message("/track/42/mute", value)
            reaper.send_message("/track/43/mute", 1 - value)
    elif track == "3":
        if poti == "gain":
            xp = [0, 0.01, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48, 0.485, 0.49, 0.495, 0.5]
            val = np.interp(value, xp, fp)
            reaper.send_message("/track/" + dj3_in + "/gain", val)
        if poti == "hi":
            val = np.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj3_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj3_cb + "/volume", val)
        if poti == "fx":
            global fxstate3
            fxstate3 = value
            sethipass()
            setlopass()
        if poti == "3d":
            reaper.send_message("/track/51/mute", value)
            reaper.send_message("/track/52/mute", 1 - value)
    elif track == "4":
        if poti == "gain":
            xp = [0, 0.01, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            fp = [0, 0.44, 0.465, 0.47, 0.475, 0.48, 0.485, 0.49, 0.495, 0.5]
            val = np.interp(value, xp, fp)
            reaper.send_message("/track/" + dj4_in + "/gain", val)
        if poti == "hi":
            val = np.interp(value, [0, 1], [0, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/hishelf/gain", val)
        if poti == "mid":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/band/0/gain", val)
        if poti == "lo":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            reaper.send_message("/track/" + dj4_in + "/fxeq/loshelf/gain", val)
        if poti == "volume":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + dj4_cb + "/volume", val)
        if poti == "fx":
            global fxstate4
            fxstate4 = value
            sethipass()
            setlopass()
        if poti == "3d":
            reaper.send_message("/track/60/mute", value)
            reaper.send_message("/track/61/mute", 1 - value)
    elif track == "master":
        if poti == "volume":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/" + masterbus + "/volume", val)
        if poti == "booth":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/1/volume", val)
        if poti == "phMix":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/22/volume", val)
            reaper.send_message("/track/21/volume", 1 - val)
            reaper.send_message("/track/20/volume", 1 - val)
            reaper.send_message("/track/19/volume", 1 - val)
            reaper.send_message("/track/18/volume", 1 - val)
        if poti == "phVol":
            val = np.interp(value, [0, 1], [0.01, 1])
            reaper.send_message("/track/14/volume", val)
    elif track == "fxmode":
        if poti == "hipass":
            if value == 1:
                global fxmodeval
                fxmodeval = "1"
                sethipass()
                setlopass()
        if poti == "lopass":
            if value == 1:
                fxmodeval = "0"
                sethipass()
                setlopass()
    elif track == "fxparm":
        if poti == "fxfreq":
            xp = [0, 1.0]
            fp = [0, 1.0]
            val = np.interp(value, xp, fp)

            reaper.send_message(
                "/track/" + dj1_in + "/fx/4/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj2_in + "/fx/4/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj3_in + "/fx/4/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj4_in + "/fx/4/fxparam/2/value", val)

            reaper.send_message(
                "/track/" + dj1_in + "/fx/5/fxparam/1/value", val)
            reaper.send_message(
                "/track/" + dj2_in + "/fx/5/fxparam/1/value", val)
            reaper.send_message(
                "/track/" + dj3_in + "/fx/5/fxparam/1/value", val)
            reaper.send_message(
                "/track/" + dj4_in + "/fx/5/fxparam/1/value", val)
        if poti == "fxres":
            val = np.interp(value, [0, 1], [0, 0.8])
            reaper.send_message(
                "/track/" + dj1_in + "/fx/5/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj2_in + "/fx/5/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj3_in + "/fx/5/fxparam/2/value", val)
            reaper.send_message(
                "/track/" + dj4_in + "/fx/5/fxparam/2/value", val)


def button_handler(address: str,
                   *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    button = words[3]
    mode = words[4]

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float

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


def vu_handler(address: str, *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[3]

    value = osc_arguments[0]

    if vu == "1":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = np.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/1/vu", val)
        # print(str(value))
    if vu == "2":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = np.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/2/vu", val)
        # print(str(value))
    if vu == "3":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = np.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/3/vu", val)
        # print(str(value))
    if vu == "4":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = np.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/4/vu", val)
        # print(str(value))
    if vu == "5":
        fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
        xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
        val = np.interp(value, xp, fp)
        ctrl_mixer.send_message("/track/5/vu", val)
        # print(str(value))


def moc_poti_handler(address: str, *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[3]
    poti = words[4]

    value = osc_arguments[0]
    # print(track + "." + poti + " : " + str(value))

    if track == "0":
        if poti == "width":
            val = np.interp(value, [0, 1], [30, 145])
            iem_1.send_message("/StereoEncoder/width", val)
            print(value)
        if poti == "side":
            val = np.interp(value, [0, 1], [0.5, 0.65])
            reaper.send_message(
                "/track/" + dj1_in + "/fx/2/fxparam/1/value", val)
    if track == "1":
        if poti == "width":
            val = np.interp(value, [0, 1], [30, 145])
            iem_2.send_message("/StereoEncoder/width", val)
            print(value)
        if poti == "side":
            val = np.interp(value, [0, 1], [0.5, 0.65])
            reaper.send_message(
                "/track/" + dj2_in + "/fx/2/fxparam/1/value", val)
    if track == "2":
        if poti == "width":
            val = np.interp(value, [0, 1], [30, 145])
            iem_3.send_message("/StereoEncoder/width", val)
            print(value)
        if poti == "side":
            val = np.interp(value, [0, 1], [0.5, 0.65])
            reaper.send_message(
                "/track/" + dj3_in + "/fx/2/fxparam/1/value", val)
    if track == "3":
        if poti == "width":
            val = np.interp(value, [0, 1], [30, 145])
            iem_4.send_message("/StereoEncoder/width", float(val))
            print(value)
        if poti == "side":
            val = np.interp(value, [0, 1], [0.5, 0.65])
            reaper.send_message(
                "/track/" + dj4_in + "/fx/2/fxparam/1/value", val)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int,
                        default=osc_router_port, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)

    # Mixer-Controller
    dispatcher.map("/mic/channel/*", poti_handler)
    dispatcher.map("/mic/channel/*", button_handler)
    dispatcher.map("/reaper/vu/*", vu_handler)

    # Motion-Controller
    dispatcher.map("/moc/channel/*", moc_poti_handler)
    # dispatcher.map("/CoordinateConverter/*", iemToCtrlMotion_handler)
    # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)
    # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
