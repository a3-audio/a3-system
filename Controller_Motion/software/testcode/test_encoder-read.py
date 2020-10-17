#!/usr/bin/python3
"""
Das wird ein test program um endlich encoder richtig aus zu lesen

@TODO: zur zeit zählt der counter im +2 pro realer Rastung
"""

from RPi import GPIO
from time import sleep

class ENCODER:

    def __init__(self, aPin, bPin,):
        """
        docstring __init__
        """
        self.aPin = aPin
        self.bPin = bPin

        GPIO.setup(self.aPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.bPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.counter = 0
        self.aLastState = GPIO.input(self.aPin)

    def read(self):
        """
        docstring read
        """
        aState = GPIO.input(self.aPin)
        bState = GPIO.input(self.bPin)
        if aState != self.aLastState:
            if bState != aState:
                    self.counter += 1
            else:
                    self.counter -= 1
           #print(self.counter)
        self.aLastState = aState

    def getCounter(self):
        """
        docstring getCounter
        """
        return self.counter

    def setCounter(self, vol):
        """
        docstring steCounter
        """
        self.counter = vol

# test
if __name__ == "__main__":
    print("Start program.")

    clk = 14
    dt = 15
    GPIO.setmode(GPIO.BCM)

    encoder = ENCODER(clk, dt)



    print("Habtschleife zum abbrechen STRG-C")
    try:

        while True:

            encoder.read()
            print(encoder.getCounter())
            sleep(0.01)

    except KeyboardInterrupt:
        print("")

    finally:
            GPIO.cleanup()
            print("Auf wieder sehen und danke für den vielen Fisch")