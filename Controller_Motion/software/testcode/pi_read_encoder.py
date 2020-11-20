#!/usr/bin/python3
"""
Wie kann man rotary encoder am Pi einlesen

"""
from ky040 import KY040
import RPi.GPIO as GPIO
import sys
import time

#### setup ####
#a1 = Button(14)
#b1 = Button(15)
#a2 = Button(23)
#b2 = Button(24)
#a3 = Button(25)
#b3 = Button(12)
#a4 = Button(16)
#b4 = Button(20)

def rotaryChange(direction):
  if direction == 1:
    print("+1")
  else:
    print("-1")

if __name__ == "__main__":

  PINA = 14
  PINB = 15 

  GPIO.setmode(GPIO.BCM)
  encoder1 = KY040(PINA, PINB, rotaryChange)
  encoder1.start()

  print("Habtschleife zum abbrechen STRG-C")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("")
  finally:
    encoder1.stop()
    GPIO.cleanup()  
    print("Auf wieder sehen und danke für den vielen Fisch")

