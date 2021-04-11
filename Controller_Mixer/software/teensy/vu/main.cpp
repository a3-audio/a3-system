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

// LED-Matrix Transform
int bar1[32][2] = {
	{0,7},
	{0,6},
	{0,5},
	{0,4},
	{0,3},
	{0,2},
	{0,1},
	{0,0},
	{1,7},
	{1,6},
	{1,5},
	{1,4},
	{1,3},
	{1,2},
	{1,1},
	{1,0},
	{2,7},
	{2,6},
	{2,5},
	{2,4},
	{2,3},
	{2,2},
	{2,1},
	{2,0},
	{3,7},
	{3,6},
	{3,5},
	{3,4},
	{3,3},
	{3,2},
	{3,1},
	{3,0}
};


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
  for (int i =0; i<8; i++) { // filter serial inputstream VU05-VU12
    for (int j=0; j<32; j++){
      lc.setLed(bar1[j][0],i,bar1[j][1],1);
      delay(5);
    }
  }
}
*/


    // Serial-Input to Pixelmatrix (Output-vu)
    if (Serial.available()) {
      String command = Serial.readStringUntil(',');
      for (int i =0; i<8; i++) { // filter serial inputstream VU05-VU12
        if(command.startsWith(vuVarsM[i])){
          String peak = Serial.readStringUntil(',');
          String rms = Serial.readStringUntil('\n');
 	  
          int peak1 = peak.toInt();// convert string to int
          //int rms1 = rms.toInt();
	  //Serial.println(rms1);
 	  
          for(int j=0;j<32;j++){//peak-meter
            lc.setLed(bar1[peak1][0],i,bar1[peak1][1],1);
	  }
        }
      }
    }
delay(20);
}	


