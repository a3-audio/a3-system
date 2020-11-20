#!/usr/bin/python3
"""
Das ist mein erster Test wie die Seril komunikation zwischen Pi und teensy funktionieren koennte.
Die lib dir ich benutze ist pySerial. https://pyserial.readthedocs.io/

zum jetzigen ziegen Zeitpunkt benutze ich noch meinen MAC, sprich der SerialPort gegebenfals angepast werden.
mit python -m serial.tools.list_ports kann man heraus finden an welchem port der Teensy angeschlossen ist.

TODO raus bekommen was die max bautrate vom teesy ist.
"""

import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "/dev/cu.usbmodem65350001"


if __name__ == "__main__":
    print("Hauptschleife wird ausgefuert, zum verlassen STG-C")
    try:
        ser.open()
        while True:
            msg = ser.readline()
            print(msg)

    except KeyboardInterrupt:
        print("")

    finally:
        ser.close()
        print("Auf Wiedersehen und danke fuer den vielen Fisch!")
