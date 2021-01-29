import jack
import numpy
from typing import List, Any
from pythonosc.udp_client import SimpleUDPClient

# OSC-Clients
ctrl_mixer = SimpleUDPClient('192.168.43.51', 8500)  # Set IP Adress
ctrl_motion = SimpleUDPClient('192.168.43.52', 8700)  # Set IP Adress

client = jack.Client('vuPy')

client.inports.register('input_1')
client.inports.register('input_2')
client.inports.register('input_3')
client.inports.register('input_4')
client.inports.register('input_5')
client.inports.register('input_6')
client.inports.register('input_7')
client.inports.register('input_8')

client.inports.register('output_1')
client.inports.register('output_2')
client.inports.register('output_3')
client.inports.register('output_4')
client.inports.register('output_5')
client.inports.register('output_6')
client.inports.register('output_7')
client.inports.register('output_8')

#ctrl_mixer.send_message("/track/1/vu", val)
#ctrl_mixer.send_message("/track/2/vu", val)
#ctrl_mixer.send_message("/track/3/vu", val)
#ctrl_mixer.send_message("/track/4/vu", val)
#ctrl_mixer.send_message("/track/5/vu", val)
#print(str(value))

#if __name__ == "__main__":

