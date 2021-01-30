import os
import threading
import signal
import sys
import jack
import numpy
from typing import List, Any
from pythonosc.udp_client import SimpleUDPClient

# OSC-Clients
ctrl_mixer = SimpleUDPClient('192.168.43.51', 8500)  # Set IP Adress
ctrl_motion = SimpleUDPClient('192.168.43.52', 8700)  # Set IP Adress

argv = iter(sys.argv)
# By default, use script name without extension as client name:
defaultclientname = os.path.splitext(os.path.basename(next(argv)))[0]

clientname = next(argv, defaultclientname)
servername = next(argv, None)

client = jack.Client(clientname, servername=servername)

if client.status.server_started:
    print('JACK server started')
if client.status.name_not_unique:
    print('unique name {0!r} assigned'.format(client.name))

event = threading.Event()

@client.set_process_callback
def process(frames):
    assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    for i, o in zip(client.inports, client.outports):
        o.get_buffer()[:] = i.get_buffer()


@client.set_shutdown_callback
def shutdown(status, reason):
    print('JACK shutdown!')
    print('status:', status)
    print('reason:', reason)
    event.set()


for x in range (0, 16):
    client.inports.register('vu_' + str(x))

with client:

    capture = client.get_ports(is_physical=True, is_output=True)
    if not capture:
        raise RuntimeError('No physical capture ports')
    
    for src, dest in zip(capture, client.inports):
        client.connect(src, dest)


    print('Press Ctrl+C to stop')
    try:
        event.wait()
    except KeyboardInterrupt:
        print('\nInterrupted by user')



#ctrl_mixer.send_message("/track/1/vu", val)
#ctrl_mixer.send_message("/track/2/vu", val)
#ctrl_mixer.send_message("/track/3/vu", val)
#ctrl_mixer.send_message("/track/4/vu", val)
#ctrl_mixer.send_message("/track/5/vu", val)
#print(str(value))

#if __name__ == "__main__":

"""
import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

for i in range(int(10*44100/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))

stream.stop_stream()
stream.close()
p.terminate()
"""



