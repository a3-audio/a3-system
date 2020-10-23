//////////////////////////////// OSC ROTARY MIXER /////////////////////////////////
//
// osc rotary mixer as it says is a piece of hardware which looks like a 4-channel
// dj-mixer with a mastersection.
//
// This is the firmware for the builtin Teensy 4.1. It uses NativeEthernet and 5x 
// hc4051 analog multiplexer. Each multiplexer is reserved for one channelstrip.
// 
// osc-data sending to Server:
//
// - /track/1-4/gain/
// - /track/1-4/hi/
// - /track/1-4/mid/
// - /track/1-4/lo/
// - /track/1-4/vol/
// - /track/1-4/pfl-button/
// - /master/1-4/hi/
// - /master/1-4/mid/
// - /master/1-4/lo/
// - /master/1-4/vol/
// - /master/1-4/pfl-button/
//
// osc-data receiving from Sever:
//
// - /led/1-5/
// - /vu/1-4/
//
// 25 x potis float 0-1
//  5 x buttons bool
//  5 x leds pfl status bool
//  4 x vu-meter
// 
///////////////////////////////////Libraries///////////////////////////////
#include <Arduino.h>
#include <SPI.h>
#include <NativeEthernet.h>
#include <NativeEthernetUdp.h>
#include <OSCBundle.h>
#include <OSCMessage.h>
/////////////////////////////Network Configuration////////////////////////

EthernetUDP Udp;                                    // Create UDP message object
byte mac[] = {0x04, 0xE9, 0xE5, 0x0C, 0x28, 0xB5};  // teensy's MAC Adress
IPAddress ip(192, 168, 43, 139);                    // teensy's IP
const unsigned int inPort  = 8500;                  // Listen port teensy

IPAddress outIp(192, 168, 43, 141);                 // destination IP
const unsigned int outPort = 9000;                  // Send port teensy

////////////////////////////////Assigning Pins/////////////////////////////
const int ledPin_1 = 41;
const int ledPin_2 = 40;
const int ledPin_3 = 39;
const int ledPin_4 = 38;
const int ledPin_5 = 27;
const int buttonPin_1 = 37;
const int buttonPin_2 = 36;
const int buttonPin_3 = 35;
const int buttonPin_4 = 34;
const int buttonPin_5 = 33;
const int analogInput_1 = 0;            // hc4051 multiplexer
const int analogInput_2 = 1;            // hc4051 multiplexer
const int analogInput_3 = 2;            // hc4051 multiplexer
const int analogInput_4 = 3;            // hc4051 multiplexer
const int analogInput_5 = 4;            // hc4051 multiplexer
const int selectPins[3] = {30, 31, 32}; // Multiplexer abc
const int vuPin_1 = 8;
const int vuPin_2 = 9;
const int vuPin_3 = 10;
const int vuPin_4 = 11;
const int vuPin_5 = 12;

// last sent states
const int num_tracks = 5;
const int num_pots = 5;

int pots_sent[num_tracks][num_pots];
int buttons_last[num_tracks];

//////////////////////////////////////OSC Server//////////////////////////////

///LED Dispatcher
void dispatchAddress_1(OSCMessage &msg){
    if (msg.isFloat(0)){
        float val = msg.getFloat(0);
            Serial.print(val);
        if (val<=0){
            digitalWrite(ledPin_1, LOW);
        }
        else if (val>=1){
            digitalWrite(ledPin_1, HIGH);
        }
    }
};

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

    Serial.begin(9600);                   // starting Serial
    Ethernet.begin(mac, ip);              // starting Ethernet
    Udp.begin(inPort);                    // starting UDP-Server

// Configurei digital pins
    pinMode(ledPin_1, OUTPUT);            // LED
    pinMode(ledPin_2, OUTPUT);            // LED
    pinMode(ledPin_3, OUTPUT);            // LED
    pinMode(ledPin_4, OUTPUT);            // LED
    pinMode(ledPin_5, OUTPUT);            // LED
    pinMode(buttonPin_1, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_2, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_3, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_4, INPUT_PULLUP);   // Pushbutton
    pinMode(buttonPin_5, INPUT_PULLUP);   // Pushbutton
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
            int analog = analogRead(track);
            int difference = pots_sent[track][pot] - analog;

            // send osc when difference larger than noise on
            // last bits
            if(abs(difference) > 6) {
                pots_sent[track][pot] = analog;

                char strAddress[64];
                sprintf(strAddress, "/track/%d/poti/%d", track+1, pot+1);

                float sendValue = float(analog) / 1023.f;

                OSCMessage message(strAddress);
                message.add(sendValue);

                Udp.beginPacket(outIp, outPort);
                message.send(Udp);
                Udp.endPacket(); 
            }
        }
    } 
    delay(80);

    // Buttons
    for(int track = 0 ; track < num_tracks ; ++track) {
        int digital = digitalRead(37 - track);

        // on rising edge send toggle
        if(digital == 1 && buttons_last[track] == 0) {
            char strAddress[64];
            sprintf(strAddress, "/button/%d", track+1);

            OSCMessage message(strAddress);
            message.add(1.f);

            Udp.beginPacket(outIp, outPort);
            message.send(Udp);
            Udp.endPacket(); 
        }

        buttons_last[track] = digital;
    }

//////////////////////////////Leds////////////////////////////////////

// TODO the leds should switch on by value 1 from osc-router if button 
// is pressed. Otherwise the led should be off:
//
// if (/track/5/recv/1/volume = 0){
//    digitalWrite(ledPin_1, LOW);
// } else HIGH
//

    //process received messages
    OSCMessage msg;
        int size;
            if ((size = Udp.parsePacket())>0){
                //fill the msg with all of the available bytes
                while(size--){
                    msg.fill(Udp.read());
                    msg.dispatch("/track/5/recv/1/volume", dispatchAddress_1);
                }
            }

// TODO the vu-meters should be build in and should do something right...

/*
    void OSCReceive(){
        OSCBundle   bundleIN;
        OSCMessage  msgIN;
        int size;
        if( (size = Udp.parsePacket())>0) {
            // if data begins with / it is a message
            if (udpData[0]==47){
                msgIN.fill(udpData,size);
                if(!msgIN.hasError()){
                    Serial.println("Receiving OSC Message...");
                    msgIN.route("/track",showMessage);
                    msgIN.route("/fx",showMessage);
                    msgIN.route("/fxparam",showMessage);
                }
            }
        }
    }
*/

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
}
