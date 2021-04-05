//#include "LedControlMS.h"
//#include "MD_MAX72xx.h"
 
//pin 18 is connected to the DataIn
//pin 14 is connected to the CLK
//pin 15 is connected to LOAD

unsigned char i;
unsigned char j;

int Max7219_pinCLK = 14;
int Max7219_pinCS = 15;
int Max7219_pinDIN = 18;

unsigned char disp1[19][8]={0x0c,0x1e,0x3e,0x7c,0x7c,0x3e,0x1e,0x0c};

void Write_Max7219_byte(unsigned char DATA)
{
  unsigned char i;
  digitalWrite(Max7219_pinCS,LOW);
  for(i=8;i>=1;i--)
  {
    digitalWrite(Max7219_pinCLK,LOW);
    digitalWrite(Max7219_pinDIN,DATA&0x80);
    DATA = DATA<<1;
    digitalWrite(Max7219_pinCLK,HIGH);
  }
}

void Write_Max7219(unsigned char address,unsigned char dat)
{
  digitalWrite(Max7219_pinCS,LOW);
  Write_Max7219_byte(address);
  Write_Max7219_byte(dat);
  digitalWrite(Max7219_pinCS,HIGH);
}

void Init_MAX7219(void)
{
  Write_Max7219(0x09, 0x00);
  Write_Max7219(0x0a, 0x03);
  Write_Max7219(0x0b, 0x07);
  Write_Max7219(0x0c, 0x01);
  Write_Max7219(0x0f, 0x00);
}

void setup()
{

  pinMode(Max7219_pinCLK,OUTPUT);
  pinMode(Max7219_pinCS,OUTPUT);
  pinMode(Max7219_pinDIN,OUTPUT);
  delay(50);
  Init_MAX7219();
}

void loop()
{
  for(j=0;j<19;j++)
  {
    for(i=1;i<9;i++)
      Write_Max7219(i,disp1[j][i-1]);
    delay(100);
  }
}
