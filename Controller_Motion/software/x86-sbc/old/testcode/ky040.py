"""
KY040 Python Class
Martin O'Hanlon
stuffaboutcode.com
Additional code added by Conrad Storz 2015 and 2016

https://github.com/conradstorz/KY040/blob/master/KY040.py
https://tutorials-raspberrypi.de/raspberry-pi-ky040-drehregler-lautstaerkeregler/

ky-040 schema
https://arduino.stackexchange.com/questions/16365/reading-from-a-ky-040-rotary-encoder-with-digispark

anpassungen an mich:
- get jetzt unter python3
- switch raus genommen

"""

import RPi.GPIO as GPIO
from time import sleep


class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    DEBOUNCE = 12

    def __init__(self, clockPin, dataPin, rotaryCallback):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.rotaryCallback = rotaryCallback


        #setup pins
        GPIO.setup(clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self._clockCallback, bouncetime=self.DEBOUNCE)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)

    
    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            self.rotaryCallback(GPIO.input(self.dataPin))
        
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)
        
        self.rotaryCallback(GPIO.input(self.dataPin))
        



#test
if __name__ == "__main__":

    print ('Program start.')

    CLOCKPIN = 26
    DATAPIN = 19

    def rotaryChange(direction):
        print ("turned - " + str(direction))

    GPIO.setmode(GPIO.BCM)
    ky040 = KY040(CLOCKPIN, DATAPIN, rotaryChange)

    print ('Launch switch monitor class.')

    ky040.start()
    print ('Start program loop...')
    try:
        while True:
            sleep(10)
            print ('Ten seconds...')
    finally:
        print ('Stopping GPIO monitoring...')
        ky040.stop()
        GPIO.cleanup()
        print ('Program ended.')