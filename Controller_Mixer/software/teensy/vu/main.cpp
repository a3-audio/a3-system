//#include "LedControl.h"
#include <Arduino.h>
 
//pin 18 is connected to the DataIn
//pin 14 is connected to the CLK
//pin 15 is connected to LOAD

/*
 Created by Rui Santos

 All the resources for this project:
 https://randomnerdtutorials.com/
*/

#include "LedControl.h"
#include "binary.h"

int bar1[32][3] = {
	{0,7,7},
	{0,7,6},
	{0,7,5},
	{0,7,4},
	{0,7,3},
	{0,7,2},
	{0,7,1},
	{0,7,0},
	{1,7,7},
	{1,7,6},
	{1,7,5},
	{1,7,4},
	{1,7,3},
	{1,7,2},
	{1,7,1},
	{1,7,0},
	{2,7,7},
	{2,7,6},
	{2,7,5},
	{2,7,4},
	{2,7,3},
	{2,7,2},
	{2,7,1},
	{2,7,0},
	{3,7,7},
	{3,7,6},
	{3,7,5},
	{3,7,4},
	{3,7,3},
	{3,7,2},
	{3,7,1},
	{3,7,0}
};

/*
 DIN connects to pin 12
 CLK connects to pin 11
 CS connects to pin 10
*/
LedControl lc=LedControl(18,14,15,4);

// delay time between faces
unsigned long delaytime=1000;

// happy face
byte hf[8]= {B00111100,B01000010,B10100101,B10000001,B10100101,B10011001,B01000010,B00111100};
// neutral face
byte nf[8]={B00111100, B01000010,B10100101,B10000001,B10111101,B10000001,B01000010,B00111100};
// sad face
byte sf[8]= {B00111100,B01000010,B10100101,B10000001,B10011001,B10100101,B01000010,B00111100};

void setup() {

  Serial.begin(115200);                 // starting Serial

  lc.shutdown(0,false);
  lc.shutdown(1,false);
  lc.shutdown(2,false);
  lc.shutdown(3,false);
  // Set brightness to a medium value
  lc.setIntensity(0,0.1);
  lc.setIntensity(1,0.1);
  lc.setIntensity(2,0.1);
  lc.setIntensity(3,0.1);
  // Clear the display
  lc.clearDisplay(0);
  lc.clearDisplay(1);
  lc.clearDisplay(2);
  lc.clearDisplay(3);
}

void clear(){
  lc.clearDisplay(0);
  lc.clearDisplay(1);
  lc.clearDisplay(2);
  lc.clearDisplay(3);
}

void drawSad(){
  // Display sad face
  lc.setRow(0,0,sf[0]);
  lc.setRow(0,1,sf[1]);
  lc.setRow(0,2,sf[2]);
  lc.setRow(0,3,sf[3]);
  lc.setRow(0,4,sf[4]);
  lc.setRow(0,5,sf[5]);
  lc.setRow(0,6,sf[6]);
  lc.setRow(0,7,sf[7]);
  delay(delaytime);
}

void drawNeutral(){
  // Display neutral face
  lc.setRow(0,0,nf[0]);
  lc.setRow(0,1,nf[1]);
  lc.setRow(0,2,nf[2]);
  lc.setRow(0,3,nf[3]);
  lc.setRow(0,4,nf[4]);
  lc.setRow(0,5,nf[5]);
  lc.setRow(0,6,nf[6]);
  lc.setRow(0,7,nf[7]);
  delay(delaytime);
}
void drawHappy(){
  // Display happy face
  lc.setRow(0,0,hf[0]);
  lc.setRow(0,1,hf[1]);
  lc.setRow(0,2,hf[2]);
  lc.setRow(0,3,hf[3]);
  lc.setRow(0,4,hf[4]);
  lc.setRow(0,5,hf[5]);
  lc.setRow(0,6,hf[6]);
  lc.setRow(0,7,hf[7]);
  delay(delaytime);
} 
/*
  lc.setLed(0,5,1,1);
  lc.setLed(1,5,1,1);
  lc.setLed(2,5,1,1);
  lc.setLed(3,5,1,1);
  delay(delaytime);
*/


void loop(){
  clear();
/*
  for (int i=0; i<32; i++){
    lc.setLed(bar1[i][0],bar1[i][1],bar1[i][2],1);
    Serial.print("hello");
    delay(5);
}
*/

  
    if (Serial.available()) {
      String command = Serial.readStringUntil(',');
      if(command.startsWith("VU1")) {
	String peak = Serial.readStringUntil(',');
	String rms = Serial.readStringUntil('\n');

	int peak1 = peak.toInt();
	int rms1 = rms.toInt();

    	Serial.print(peak1 + rms1);
  	lc.setLed(bar1[2][0],bar1[2][1],bar1[2][2],1);
  	}
    }

  delay(500);
  
}
