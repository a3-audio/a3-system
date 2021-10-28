// This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
// © Copyright 2021 Jendrik Bradaczek 

/*
um es später schön zu machen:

Bounce pushbutton = Bounce(PIN_BUTTON_ENCODER, 10);
pinMode(PIN_BUTTON_ENCODER, INPUT_PULLUP);
  if (pushbutton.update())
  {
    if (pushbutton.fallingEdge())
    {
        // ...
    }
  }
*/

#include <Arduino.h>
#include <Encoder.h>
#include <Adafruit_NeoPixel.h>

// Multiplexer In/Out Pin's
#define muxInBtnMx1 20 //Butten Matrix
#define muxInBtnMx2 19 //Butten Matrix
#define muxInPot 18    //Poti in
#define muxInBtnEncoder 8 //Encoder Buttons in

// Multiplexer address Pin's (s0/s1/s2)
#define s0 23 // low-order bit
#define s1 22
#define s2 21 // high-order bit

// Encoder Pin's
#define enc0_DT 0
#define enc0_CLK 1
#define enc1_DT 2
#define enc1_CLK 3
#define enc2_DT 4
#define enc2_CLK 5
#define enc3_DT 6
#define enc3_CLK 7

// NeoPixel
#define npxl_pin 9
#define npxl_leds 16
Adafruit_NeoPixel strip = Adafruit_NeoPixel(npxl_leds, npxl_pin, NEO_GRB + NEO_KHZ800);

// multipexer adrress Bit
bool addrBit0 = 0;
bool addrBit1 = 0;
bool addrBit2 = 0;

// btnMatrx arry
bool btnMxNew[16];
bool btnMxOld[16];

// poti arry
int potiNew[8];
int potiOld[8];

// BtnEncoder
bool btnEncoderNew[8];
bool btnEncoderOld[8];

// Encoder def
Encoder enc0(enc0_DT, enc0_CLK);
Encoder enc1(enc1_DT, enc1_CLK);
Encoder enc2(enc2_DT, enc2_CLK);
Encoder enc3(enc3_DT, enc3_CLK);

long posEnc0 = 0;
long posEnc1 = 0;
long posEnc2 = 0;
long posEnc3 = 0;

long newEnc0 = 0;
long newEnc1 = 0;
long newEnc2 = 0;
long newEnc3 = 0;

void initBtnMatrix()
{
  // btnMatrix init
  for (byte i = 0; i < 16; i++)
  {
    btnMxNew[i] = 0;
    btnMxOld[i] = 0;
  }
}

void sendBtnMx()
{
  for (byte i = 0; i < 16; i++)
  {
    if (btnMxNew[i] != btnMxOld[i])
    {
      Serial.print("B");
      Serial.print(i);
      Serial.print(":");
      Serial.println(btnMxNew[i]);
      btnMxOld[i] = btnMxNew[i];
    }
  }
}



void initPoti()
{
  pinMode(muxInBtnMx1, INPUT_PULLDOWN);
  pinMode(muxInBtnMx2, INPUT_PULLDOWN);
  for (byte i = 0; i < 8; i++)
  {
    potiNew[i] = 0;
    potiOld[i] = 0;
  }
}

void sendPoti()
{
  for (byte i = 0; i < 8; i++)
  {
    if (abs(potiNew[i] - potiOld[i]) > 3)
    {
      Serial.print("P");
      Serial.print(i);
      Serial.print(":");
      Serial.println(potiNew[i]);
      potiOld[i] = potiNew[i];
    }
  }
}

void readMux()
{
  for (byte i = 0; i < 8; i++)
  {
    addrBit0 = bitRead(i, 0);
    addrBit1 = bitRead(i, 1);
    addrBit2 = bitRead(i, 2);
    digitalWrite(s0, addrBit0);
    digitalWrite(s1, addrBit1);
    digitalWrite(s2, addrBit2);
    delayMicroseconds(50); // Damit der 4051 zeit hat die Adresse um zu schalten

    // read Butten Matrix
    btnMxNew[i] = digitalRead(muxInBtnMx1);
    btnMxNew[i + 8] = digitalRead(muxInBtnMx2);

    // read Butten Encoder
    btnEncoderNew[i] = digitalRead(muxInBtnEncoder);

    // read the Poti's
    potiNew[i] = analogRead(muxInPot);
  }
}

void initBtnEncoder()
{
  for (byte i = 0; i < 4; i++)
  {
    btnEncoderNew[i] = 0;
    btnEncoderOld[i] = 0;
  }
}

void sendBtnEncoder()
{
  for (byte i = 0; i < 4; i++)
  {
    if (btnEncoderNew[i] != btnEncoderOld[i])
    {
      Serial.print("EB");
      Serial.print(i);
      Serial.print(":");
      Serial.println(btnEncoderNew[i]);
      btnEncoderOld[i] = btnEncoderNew[i];
    }
  }
}

void readEncoder()
{
  newEnc0 = enc0.read();
  newEnc1 = enc1.read();
  newEnc2 = enc2.read();
  newEnc3 = enc3.read();
}

void sendEncoder()
{
  if (newEnc0 != posEnc0)
  {
    Serial.print("Enc0:");
    Serial.println(newEnc0);
    posEnc0 = newEnc0;
  }

  if (newEnc1 != posEnc1)
  {
    Serial.print("Enc1:");
    Serial.println(newEnc1);
    posEnc1 = newEnc1;
  }

  if (newEnc2 != posEnc2)
  {
    Serial.print("Enc2:");
    Serial.println(newEnc2);
    posEnc2 = newEnc2;
  }

  if (newEnc3 != posEnc3)
  {
    Serial.print("Enc3:");
    Serial.println(newEnc3);
    posEnc3 = newEnc3;
  }
}

void receivePixels(){
  if (Serial.available()) {
    String command = Serial.readStringUntil(',');
    if(command.startsWith("L")) {
      int pixNum  = Serial.readStringUntil(',').toInt();
      int red = Serial.readStringUntil(',').toInt();
      int green = Serial.readStringUntil(',').toInt();
      int blue  = Serial.readStringUntil('\n').toInt();

      strip.clear();
      strip.setPixelColor(pixNum, strip.Color(green, red, blue));
      strip.show(); // This sends the updated pixel color to the hardware.
    }
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10);
  while (!Serial)
  {
    ; // wait for serial conaction
  }
  Serial.println("#######################################");
  Serial.println("          controller connected");
  Serial.println("#######################################");

  initBtnMatrix();
  initBtnEncoder();
  initPoti();

  strip.begin();

}

void loop()
{
  readMux();
  readEncoder();

  sendBtnMx();
  sendBtnEncoder();
  sendEncoder();
  sendPoti();

  receivePixels();
}
