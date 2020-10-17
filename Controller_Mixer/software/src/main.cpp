//////////////////////////////// OSC ROTARY MIXER /////////////////////////////////
//
// Zu diesr Software gehört ein Stück Hardware was aussieht wie ein DJ-Mixer.
// Ziel ist es, mit diesem Stück einen Softwaremixer via OSC fernzubedienen,
// ein Controller...
//
// Im Mixer steckt ein Teensy 4.1 mit Netzwerkschnittstelle und 5x hc4051 
// analog multiplexer.
// 
// Diese osc-Adressen soll er senden:
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
// Diese osc-Adressen soll er empfangen:
//
// - /led/1-5/
// - /vu/1-4/
//
// 25 x potis float 0-1
//  5 x buttons bool
//  5 x leds pfl status bool
//  4 x vu-meter
// 
// Notiz: Aktuell sendet teensy durchgehend osc. treshhold einbauen...
// Notiz: https://www.pjrc.com/teensy/td_midi.html (multiplexer)
//
// Raphael Eismann
// r.eismann@posteo.de
//
// contributers:
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
const unsigned int inPort  = 8000;                  // Listen port teensy

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

//////////////////////////////////osc receiver/////////////////////////////////
//
// converts the pin to an osc address
/*
  char * numToOSCAddress( int pin){
  static char s[5];
  int i = 4;

  s[i--]= '\0';
  do
  {
  s[i] = "01234"[pin % 5];
  --i;
  pin /= 5;
  }
  while(pin && i);
  s[i] = '/';
  return &s[i];
  }

  void routeLed(OSCMessage &msg, int addrOffset ){
  //iterate through all the analog pins
  for(byte pin = 0; pin < 5; pin++){
  //match against the pin number strings
  int pinMatched = msg.match(numToOSCAddress(pin), addrOffset);
  if(pinMatched){
  unsigned int led_1 = 0;
  unsigned int led_2 = 0;
  unsigned int led_3 = 0;
  unsigned int led_4 = 0;
  unsigned int led_5 = 0;
  //if it has an int, then it's an integers frequency in Hz
  for(int i=0; i<5; i++){ 
  if (msg.isInt(i)){        
  led_1 = msg.getInt(i);
  } 
  }
  }
  }
  }


  // Button 1
  buttonState_1 = digitalRead(buttonPin_1);
  if(buttonState_1 == LOW && x_1 == 1)
  {
  digitalWrite(ledPin_1, HIGH);
  delay(btn_delay);
  x_1 = 0;
  Serial.print("btn 1");
  }
  else if (buttonState_1 == LOW && x_1 == 0)
  {
  digitalWrite(ledPin_1, LOW);
  delay(btn_delay);
  x_1 = 1;
  }

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

// Jeder Kanalzug am Controller reserviert einen 8-fach Multiplexer (hc4051).
//
// Wir haben am Controller 4 Eingangskanäle und den Masterikanal. Die mps sind 
// über die Stellbits gleichgeschaltet. 
//
// getaktet und über die analogPins (siehe oben) 
// angesclossen.    

    // OSCBundle bndl;

    // Potis
    // hc4051 reading potis
    for (byte pot=0 ; pot <= 4; pot++)     
    {
        // hc4051 pinselector abc (binär)
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
    // bndl.add("/button/1").add((digitalRead(37)==HIGH)?0:1);
    // bndl.add("/button/2").add((digitalRead(36)==HIGH)?0:1);
    // bndl.add("/button/3").add((digitalRead(35)==HIGH)?0:1);
    // bndl.add("/button/4").add((digitalRead(34)==HIGH)?0:1);
    // bndl.add("/button/5").add((digitalRead(33)==HIGH)?0:1);


//////////////////////////////Buttons///////////////////////////////////
//
// Der Toggle zur statusanzeige (osc vom host)
//
//



    /*
    //process received messages
    OSCMessage msg;
    SLIPEncodedSerial = SLIPSerial(Serial);
    while(!SLIPSerial.endofPacket()){
    int size = SLIPSerial.available();
    if (size > 0){
    //fill the msg with all of the available bytes
    while(size--){
    msg.fill(SLIPSerial.read());
    }
    }
    }

    //returns true if the data in the first position is an integer
    if (msg.isInt(0)){
    //get that integer
    int data = msg.getInt(0);
    }

    OSCMessage msg("/a/1");
    msg.dispatch("/a/1", dispatchAddress);
    
    //called whenever an OSCMessage's address matches "/a/1"
    void dispatchAddress(OSCMessage &msg){
    //do something with the OSCMessage...
    if (msg.isFloat(0)){
    float val = msg.getFloat(0);
    }
    }
    */
/*
  int btn_delay = 500;

  // Button 1
  buttonState_1 = digitalRead(buttonPin_1);
  if(buttonState_1 == LOW && x_1 == 1)
  {
  digitalWrite(ledPin_1, HIGH);
  delay(btn_delay);
  x_1 = 0;
  Serial.print("btn 1");
  }
  else if (buttonState_1 == LOW && x_1 == 0)
  {
  digitalWrite(ledPin_1, LOW);
  delay(btn_delay);
  x_1 = 1;
  }


  //Button 2
  buttonState_2 = digitalRead(buttonPin_2);
  if(buttonState_2 == LOW && x_2 == 1)
  {
  digitalWrite(ledPin_2, HIGH);
  delay(btn_delay);
  x_2 = 0;
  Serial.print("btn 2");
  }
  else if (buttonState_2 == LOW && x_2 == 0)
  {
  digitalWrite(ledPin_2, LOW);
  delay(btn_delay);
  x_2 = 1;
  }
  // Button 3
  buttonState_3 = digitalRead(buttonPin_3);
  if(buttonState_3 == LOW && x_3 == 1)
  {
  digitalWrite(ledPin_3, HIGH);
  delay(btn_delay);
  x_3 = 0;
  Serial.print("btn 3");
  }
  else if (buttonState_3 == LOW && x_3 == 0)
  {
  digitalWrite(ledPin_3, LOW);
  delay(btn_delay);
  x_3 = 1;
  }
  // Button 4
  buttonState_4 = digitalRead(buttonPin_4);
  if(buttonState_4 == LOW && x_4 == 1)
  {
  digitalWrite(ledPin_4, HIGH);
  delay(btn_delay);
  x_4 = 0;
  Serial.print("btn 4");
  }
  else if (buttonState_4 == LOW && x_4 == 0)
  {
  digitalWrite(ledPin_4, LOW);
  delay(btn_delay);
  x_4 = 1;
  }
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
/*
  void OSCReceive(){
  OSCBundle   bundleIN;
  OSCMessage  msgIN;
  int size;
  if( (size = Udp.parsePacket())>0) {
  byte udpData[size];
  for (int i=0;i<size;i++) udpData[i]=Udp.read();
  // if data begins with # it is a bundle
  if (udpData[0]==35){
  bundleIN.fill(udpData,size);
  if(!bundleIN.hasError()) {
  Serial.println("Receiving OSC Bundle...");
  bundleIN.route("/track", showMessage);
  bundleIN.route("/fx", showMessage);
  bundleIN.route("/fxparam", showMessage);
  }
  }
  // if data begins with / it is a message
  else if (udpData[0]==47){
  msgIN.fill(udpData,size);
  if(!msgIN.hasError()){
  Serial.println("Receiving OSC Message...");
  msgIN.route("/track",showMessage);
  msgIN.route("/fx",showMessage);
  msgIN.route("/fxparam",showMessage);
  }
  }
  }
*/
}
