#!/usr/bin/python3
import sys
import time
# import für die Analogen eingänge
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
# import für OSC
from pythonosc.udp_client import SimpleUDPClient

########### setup ############
# AnalogInput
# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
analogIn = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

############## OSC ##################

#server address
ip = "192.168.43.129"

#non-mixer osc-port
port_mixer = 9000

#IEM plugins
port_enc_dj1 = 1337
port_enc_dj2 = 1338
port_enc_dj3 = 1339
port_enc_dj4 = 1340

client_mixer = SimpleUDPClient(ip, port_mixer)
client_enc_dj1 = SimpleUDPClient(ip, port_enc_dj1)
client_enc_dj2 = SimpleUDPClient(ip, port_enc_dj2)
client_enc_dj3 = SimpleUDPClient(ip, port_enc_dj3)
client_enc_dj4 = SimpleUDPClient(ip, port_enc_dj4)



# init var
voluesNew = [0] * 8
voluesOld = [0] * 8

ema_a =0.4
ema_s = [0] * 8

print("Habtschleife zum abbrechen STRG-C")
try:
    for i in range(8):
        ema_s[i] = analogIn.read_adc(i)

    while True:
        # Poties auslesen
        for i in range(8):
            sensorValue = analogIn.read_adc(i)
            ema_s[i] = (ema_a * sensorValue) + ((1 - ema_a) * ema_s[i])
            voluesNew[i] = int(ema_s[i])
            if abs(voluesNew[i] - voluesOld[i]) >= 2 :
                #Hier wird dan OSC gesendet
                if i == 0:
                    client_mixer.send_message("/strip/DJ1/Aux%20(B)/Gain%20(dB)", voluesNew[i]/1024)
                    client_mixer.send_message("/strip/DJ1/Gain.1/Gain%20(dB)", 1 - voluesNew[i]/1024)
                if i == 1:
                    client_mixer.send_message("/strip/DJ2/Aux%20(B)/Gain%20(dB)", voluesNew[i]/1024)
                    client_mixer.send_message("/strip/DJ2/Gain.1/Gain%20(dB)", 1 - voluesNew[i]/1024)
                if i == 2:
                    client_mixer.send_message("/strip/DJ3/Aux%20(B)/Gain%20(dB)", voluesNew[i]/1024)
                    client_mixer.send_message("/strip/DJ3/Gain.1/Gain%20(dB)", 1 - voluesNew[i]/1024)
                if i == 3:
                    client_mixer.send_message("/strip/DJ4/Aux%20(B)/Gain%20(dB)", voluesNew[i]/1024)
                    client_mixer.send_message("/strip/DJ4/Gain.1/Gain%20(dB)", 1 - voluesNew[i]/1024)
                if i == 4:
                    pass
                if i == 5:
                    pass
                if i == 6:
                    pass
                if i == 7:
                    pass

                print("Porti", str(i), str(voluesNew[i]))
            voluesOld[i] = voluesNew[i]

        time.sleep(1/60)
except KeyboardInterrupt:
    print("")
finally:
    print("Auf wieder sehen und danke für den vielen Fisch")
