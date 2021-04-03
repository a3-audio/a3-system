#include <Arduino.h>

////////////////////////////////Assigning Pins/////////////////////////////
const int ledPin_1 = 26;
const int ledPin_2 = 38;
const int ledPin_3 = 39;
const int ledPin_4 = 40;
const int ledPin_5 = 41;
/*
const int buttonPin_1 = 33;
const int buttonPin_2 = 34;
const int buttonPin_3 = 35;
const int buttonPin_4 = 36;
const int buttonPin_5 = 37;
*/
const int pflButtons[5] = {33, 34, 35, 36, 37}; // PFL-Button pins
const int multiplexer[5] = {5, 6, 7, 8, 9}; // Multiplexer pins
const int selectPins[3] = {30, 31, 32}; // Multiplexer abc
/*
const int vuPin_1 = 19;
const int vuPin_2 = 20;
const int vuPin_3 = 21;
const int vuPin_4 = 22;
const int vuPin_5 = 23;
*/
// last sent states
const int num_tracks = 5;
const int num_pots = 5;

int pots_sent[num_tracks][num_pots];
int buttons_last[num_tracks];

///////////////////////////////////////Setup///////////////////////////////////
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

    Serial.begin(115200);                 // starting Serial

// Configure digital pins
    
    for(int track = 0 ; track < num_tracks ; ++track) {
        pinMode(pflButtons[track], OUTPUT);
    }
    pinMode(ledPin_1, OUTPUT);            // LED
    pinMode(ledPin_2, OUTPUT);            // LED
    pinMode(ledPin_3, OUTPUT);            // LED
    pinMode(ledPin_4, OUTPUT);            // LED
    pinMode(ledPin_5, OUTPUT);            // LED
    /*
    pinMode(buttonPin_1, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_2, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_3, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_4, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_5, INPUT_PULLUP);   // Pushbutton
    */
/*
// configure analog pins
    pinMode(vuPin_1, OUTPUT);             // VU-METER
    pinMode(vuPin_2, OUTPUT);             // VU-METER
    pinMode(vuPin_3, OUTPUT);             // VU-METER
    pinMode(vuPin_4, OUTPUT);             // VU-METER
    pinMode(vuPin_5, OUTPUT);             // VU-METER
*/
}
////////////////////////////////////////LOOP////////////////////////////////////
void loop(){
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
    delay(80);
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

