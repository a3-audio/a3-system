/*


um es spaeter schon zu machen:

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

// Multiplexer In/Out line
#define muxIn1 20 //Butten Matrix
#define muxIn2 19 //Butten Matrix

// Multiplexer address (s0/s1/s2)
#define s0 23 // low-order bit
#define s1 22
#define s2 21 // high-order bit

// multipexer adrress Bit
bool addrBit0 = 0;
bool addrBit1 = 0;
bool addrBit2 = 0;

// btnMatrx arry
bool btnMatrixNew[16];
bool btnMatrixOld[16];

void btnMatrixInit()
{
  // btnMatrix init
  for (byte i = 0; i < 16; i++)
  {
    btnMatrixNew[i] = 0;
    btnMatrixOld[i] = 0;
  }
}

void muxRead()
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
    btnMatrixNew[i] = digitalRead(muxIn1);
    btnMatrixNew[i + 8] = digitalRead(muxIn2);
  }
}

// MAIN
void setup()
{
  Serial.begin(115200);
  while (!Serial)
  {
    ; // wait for serial conaction
  }
  Serial.println("contoller conected");

  pinMode(muxIn1, INPUT_PULLDOWN);
  pinMode(muxIn2, INPUT_PULLDOWN);

  btnMatrixInit();

} // end of setup

void loop()
{
  muxRead();
  for (byte i = 0; i < 16; i++)
  {
    if (btnMatrixNew[i] != btnMatrixOld[i])
    {
      Serial.print("B");
      Serial.print(i);
      Serial.print(":");
      Serial.println(btnMatrixNew[i]);
      btnMatrixOld[i] = btnMatrixNew[i];
    }
  }
} // end of loop
