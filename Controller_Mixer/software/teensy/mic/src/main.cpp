#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

// AAA-MIXER / Teensy Firmare for PCB v0.2

// Assigning pins
const int ledPin_1 = 26;// pfl-leds
const int ledPin_2 = 38;
const int ledPin_3 = 39;
const int ledPin_4 = 40;
const int ledPin_5 = 41;
const int pflButtons[5] = {33, 34, 35, 36, 37}; // PFL-Button 
const int multiplexer[5] = {5, 6, 7, 8, 9}; // Poti pins
const int selectPins[3] = {30, 31, 32}; // Multiplexer abc
const int npxl_pin = 13;
const int npxl_leds = 48;

// last sent states (potis)
const int num_tracks = 5;
const int num_pots = 5;
int pots_sent[num_tracks][num_pots];
int buttons_last[num_tracks];

// NeoPixel
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(npxl_leds, npxl_pin, NEO_GRB + NEO_KHZ800);

// NeoPixel Arrays
String vuVars[4] = { "VU01", "VU02", "VU03", "VU04" };

int vupxlstrips[4][9] = {
{11,10,9,8,7,6,5,4,3},
{23,22,21,20,19,18,17,16,15}, 
{35,34,33,32,31,30,29,28,27}, 
{47,46,45,44,43,42,41,40,39} 
};

void setup() {

    // initialize sent values to 0
    for(int track = 0 ; track < num_tracks ; ++track) {
        for(int pot = 0 ; pot < num_pots ; ++pot) {
            pots_sent[track][pot] = 0;
        }
    }

    // initialize button state to 0
    for(int track = 0 ; track < num_tracks ; ++track) {
        buttons_last[track] = 0;
    }

    Serial.begin(115200);       // starting Serial
    pixels.begin(); 		// INITIALIZE NeoPixel
    pixels.clear();
    pixels.setBrightness(10);

// Configure digital pins
    
    for(int track = 0 ; track < num_tracks ; ++track) {
        pinMode(pflButtons[track], OUTPUT);
    }
    pinMode(ledPin_1, OUTPUT);            // LED
    pinMode(ledPin_2, OUTPUT);            // LED
    pinMode(ledPin_3, OUTPUT);            // LED
    pinMode(ledPin_4, OUTPUT);            // LED
    pinMode(ledPin_5, OUTPUT);            // LED
}

void loop(){
    pixels.clear();
    // hc4051 reading potis
    for (byte pot=0 ; pot <= 4; pot++)     
    {
        // hc4051 pinselector abc (binary)
        for (int i=0; i<3; i++) {     
            digitalWrite(selectPins[i], pot & (1 << i)?HIGH:LOW); // select hc4051
        }
        delayMicroseconds(50);
        // filter analog inputs
        for (int track=0 ; track < 5; track++) {
            int analog = analogRead(multiplexer[track]);
            int difference = pots_sent[track][pot] - analog;

            // send osc when difference larger than noise on
            // last bits
            if(abs(difference) > 6) {
                pots_sent[track][pot] = analog;
                float sendValue = float(analog) / 1023.f;
                Serial.print("T");
                Serial.print(":");
                Serial.print(track+1);
                Serial.print(":");
                Serial.print("P");
                Serial.print(":");
                Serial.print(pot+1);
                Serial.print(":");
                Serial.println(sendValue);
            }
        }
    } 
    delayMicroseconds(50);

    // Buttons
    for(int track = 0 ; track < num_tracks ; ++track) {
        int digital = digitalRead(pflButtons[track]);

        // on rising edge send toggle
        if(digital == 1 && buttons_last[track] == 0) {
            Serial.print("T");
            Serial.print(":");
            Serial.print(track+1);
            Serial.print(":");
            Serial.print("B");
            Serial.print(":");
            Serial.print("0");
            Serial.print(":");
            Serial.println("0");
        }

        buttons_last[track] = digital;
    }

    if (Serial.available()) {
      String command = Serial.readStringUntil('\n');
      if(command.startsWith("L1")) {
        digitalWrite(ledPin_1, HIGH);
        digitalWrite(ledPin_2, LOW);
        digitalWrite(ledPin_3, LOW);
        digitalWrite(ledPin_4, LOW);
        digitalWrite(ledPin_5, LOW);
      }
      if(command.startsWith("L2")) {
        digitalWrite(ledPin_1, LOW);
        digitalWrite(ledPin_2, HIGH);
        digitalWrite(ledPin_3, LOW);
        digitalWrite(ledPin_4, LOW);
        digitalWrite(ledPin_5, LOW);
      }
      if(command.startsWith("L3")) {
        digitalWrite(ledPin_1, LOW);
        digitalWrite(ledPin_2, LOW);
        digitalWrite(ledPin_3, HIGH);
        digitalWrite(ledPin_4, LOW);
        digitalWrite(ledPin_5, LOW);
      }
      if(command.startsWith("L4")) {
        digitalWrite(ledPin_1, LOW);
        digitalWrite(ledPin_2, LOW);
        digitalWrite(ledPin_3, LOW);
        digitalWrite(ledPin_4, HIGH);
        digitalWrite(ledPin_5, LOW);
      }
      if(command.startsWith("L5")) {
        digitalWrite(ledPin_1, LOW);
        digitalWrite(ledPin_2, LOW);
        digitalWrite(ledPin_3, LOW);
        digitalWrite(ledPin_4, LOW);
        digitalWrite(ledPin_5, HIGH);
      }
    }

    // NeoPixel Input-vu
    if (Serial.available()) {
      String command = Serial.readStringUntil(',');
      for (int i =0; i<4; i++) { // filter serial inputstream VU01-VU04
        if(command.startsWith(vuVars[i])) {
          String peak = Serial.readStringUntil(',');
          String rms = Serial.readStringUntil('\n');
 	  
          int peak1 = peak.toInt();// convert string to int
          int rms1 = rms.toInt();
 	  
          for(int j=0;j<9;j++){// peakmeter 
            pixels.setPixelColor(vupxlstrips[i][peak1], pixels.Color(255,000,000));
	    for(int k=0;k<9;k++){// rms-meter
              if(k<rms1){
                pixels.setPixelColor(vupxlstrips[i][k], pixels.Color(000,255,000));
              }
            }
          }
        }
      }
    }

    delayMicroseconds(20);
    pixels.show(); // send to hardware.
}

/*
  // Button 5
  buttonState_5 = digitalRead(buttonPin_5);
  if(buttonState_5 == LOW && x_5 == 1)
  {
  digitalWrite(ledPin_5, HIGH);
  delay(btn_delay);
  x_5 = 0;
  Serial.print("btn 5");
  }
  else if (buttonState_5 == LOW && x_5 == 0)
  {
  digitalWrite(ledPin_5, LOW);
  delay(btn_delay);
  x_5 = 1;
  }
*/

