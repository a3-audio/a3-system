/*
 * main.h
 *
 * Created: 27/02/2022 00:02:29
 *  Author: tirii
 */ 


#ifndef MAIN_H_
#define MAIN_H_
#include "src/hardware.h"
#include "src/bitoperation.h"
#include "src/ledandcolor.h"
//#include "src/debug.h"
#include "src/button.h"
//#include "src/encoder.h"
#include "src/timer.h"
//#include "src/adc.h"
#include "src/i2c.h"


#define TIME_ABOVE(colorval,colortime,bitpos)	((!!(colorval>colortime))<<bitpos)



#define EVENT_LEDS1B			12
#define EVENT_LEDS1R			1
#define EVENT_LEDS1G			2
#define EVENT_LEDS2B			3
#define EVENT_LEDS2R			4
#define EVENT_LEDS2G			5
#define EVENT_LEDS3B			6
#define EVENT_LEDS3R			7
#define EVENT_LEDS3G			8
#define EVENT_LEDS4B			9
#define EVENT_LEDS4R			10
#define EVENT_LEDS4G			11
#define EVENT_COUNTER_OVERFLOW	0
#define EVENT_LED_ACK_ON		13
#define EVENT_LED_ACK_OFF		14
#define EVENT_LED_SENDING		15



#define EVENT_BUT0_PRESS	0
#define EVENT_BUT0_RELEASE	1
#define EVENT_BUT1_PRESS	2
#define EVENT_BUT1_RELEASE	3
#define EVENT_BUT2_PRESS	4
#define EVENT_BUT2_RELEASE	5
#define EVENT_BUT3_PRESS	6
#define EVENT_BUT3_RELEASE	7






void led_shiftSend(uint16_t data);

int8_t encode_read( uint8_t step );
 //converts an angle and a intensity value to RGB
 //angle is 0-360 and val 0-255




/*
for color conversion hsv to RGB
H is angle 
S is satuartion
V is lumiation
C=V*S
x=c*(1-|(h/60)mod2-1|) mod2 means remainder when divided by two
						->360-179 & 180-359 = 0-1.9999...
m=V-C
r g b
C X 0	60
X C 0   120
0 C X   180
0 X C   240
X 0 C   300
C 0 X   360

R=(r+m)*255
G=(g+m)*255
B=(b+m)*255




*/



#endif /* MAIN_H_ */
