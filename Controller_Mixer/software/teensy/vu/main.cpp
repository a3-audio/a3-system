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
  clear();

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
    for (int i = 0 ; i < 8 ; i++) { // filter serial inputstream VU05-VU12
      if(command.startsWith(vuVarsM[i]))
      {
        String peak = Serial.readStringUntil(',');
        String rms = Serial.readStringUntil('\n');
 	  
        int peak_index = peak.toInt();// convert string to int
        //int rms1 = rms.toInt();
        //Serial.println(rms1);

        peak_index = 32;

        // peak-meter
        for(int j = 0 ; j <= peak_index ; j++){
          int module_index = j / 8;
          int x = i;
          int y = j % 8;
          lc.setLed(module_index, x, y, true);
        }
      }
    }
  }

  delay(20);
}	
