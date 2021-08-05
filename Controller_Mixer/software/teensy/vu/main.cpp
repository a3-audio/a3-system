// © Copyright 2021 A³ Ambisonic Audio Adventures UG (Haftungsbeschränkt). 
// This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING

#include <Arduino.h>
#include <LedControl.h>
#include <binary.h>
#include <Adafruit_NeoPixel.h>

//pin 18 is connected to the DataIn
//pin 14 is connected to the CLK
//pin 15 is connected to LOAD

// define LED-Matrix 
LedControl lc=LedControl(18,14,15,4);

// LED-Matrix Inputs
String vuVarsM[8] = { "VU05", "VU06", "VU07", "VU08", "VU09", "VU10", "VU11", "VU12" };

void setup() {

  // starting Serial	
  Serial.begin(115200);

  // prevent LED-Matrix from Powersafe
  lc.shutdown(0,false);
  lc.shutdown(1,false);
  lc.shutdown(2,false);
  lc.shutdown(3,false);

  // Set brightness
  lc.setIntensity(0,1);
  lc.setIntensity(1,1);
  lc.setIntensity(2,1);
  lc.setIntensity(3,1);
}

void clear(){
  lc.clearDisplay(0);
  lc.clearDisplay(1);
  lc.clearDisplay(2);
  lc.clearDisplay(3);
}

void loop(){
  // clear();

  /*
  // Pixelmatrix Test
  for (int i = 0; i < 8 ; i++) {
    for (int j = 0 ; j < 32 ; j++) {
      int module_index = j / 8;
      int x = i;
      int y = j % 8;

      lc.setLed(module_index, x, y, true);
      delay(5);
    }
  }
  */

  // Serial-Input to Pixelmatrix (Output-vu)
  if (Serial.available())
  {
    String command = Serial.readStringUntil(',');
    if(!command.startsWith("VU"))
    {
      Serial.readStringUntil('\n');
      return;
    }

    for (int i = 0 ; i < 8 ; i++) { // filter serial inputstream VU05-VU12
      if(command.startsWith(vuVarsM[i]))
      {
        String peak = Serial.readStringUntil(',');
        String rms = Serial.readStringUntil('\n');
        // String peak = "31";
        // String rms = "31";

        int peak_index = peak.toInt();
        int rms_index = rms.toInt();
        //Serial.println(rms1);

        // rms-meter plus peak over all leds
        for(int j = 0 ; j < 32 ; j++){
          int module_index = j / 8;
          int x = i;
          int y = 7 - j % 8;

          bool led_on = j <= rms_index || j == peak_index;
          lc.setLed(module_index, x, y, led_on);
        }
      }
    }
  }
}
