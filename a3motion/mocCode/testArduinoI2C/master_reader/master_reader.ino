// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>
uint8_t t = 0;
uint32_t count=0;
uint32_t avg=0;
uint32_t avgArr[32];
uint32_t sum=0;
void setup() {
  Wire.begin();  // join i2c bus (address optional for master)
  //Wire.setClock(100000);
  Serial.begin(9600);  // start serial for output
/*
  for(int i=1;i<=100;i++){
      Wire.beginTransmission(4);
  Wire.write(33);
  Wire.endTransmission();
  delayMicroseconds(500);  //}
   Wire.requestFrom(4, 2);  // request 6 bytes from slave device #8
     uint16_t retVal[2];
    uint8_t iRetVal = 0;
    while (Wire.available()) {  // slave may send less than requested
      uint8_t c = Wire.read();  // receive a byte as character
      retVal[iRetVal] = c;
      iRetVal++;
      iRetVal %= 2;
    }
    uint16_t tes=((retVal[0]&0x0F)<<8)|retVal[1];
    Serial.print(tes,DEC);
    if(i%20==0)
    Serial.print("\n");
    else
    Serial.print(" ");
    sum+=tes;
    delay(5);
  }
  avg=sum/100;
  Serial.print("avg ");
  Serial.println(avg,DEC);
  count=0;
  sum=0;*/
  Serial.println("hallo");
}

void loop() {


  
  //count++;
  //count%=32;
   Serial.println("hallo");
  Wire.requestFrom(4, 1);  // request 6 bytes from slave device #8
  uint16_t retVal[2];
  uint8_t iRetVal = 0;
  while (Wire.available()) {  // slave may send less than requested
    uint8_t c = Wire.read();  // receive a byte as character
    retVal[iRetVal] = c;
    iRetVal++;
    iRetVal %= 2;
  }
  /*uint16_t tes=((retVal[0]&0x0F)<<8)|retVal[1];
  sum-=avgArr[count];
  avgArr[count]=abs((int32_t)avg-tes);
  sum+=avgArr[count];*/
Serial.println(retVal[0],DEC);
//Serial.println(abs((int32_t)avg-tes),DEC);

 // Serial.println(sum/count,DEC);  // print the character
  delay(300);
}
