/*
 * colormath.h
 *
 * Created: 16/03/2022 13:13:26
 *  Author: tirii
 */ 


#ifndef COLORMATH_H_
#define COLORMATH_H_
#include "hardware.h"

#define LED_MAX 255


typedef struct{
	uint16_t shiftVal;
	uint8_t time;
} ledEvent;

typedef	struct{
	uint8_t	position;
	uint8_t time;
}led;

typedef struct{
	uint8_t *newTime;
	led		ledVal;
}ledStruct;


typedef struct
 {
	 led	red;
	 led	green;
	 led	blue;
 }rgbLed;
 
void led_updateRGB(uint8_t number,uint16_t angle,uint8_t value);
void led_rgbInit();
void led_hsvToRGB (rgbLed *regButton,float angle, uint8_t val);
void led_updateColorSystem();
int led_Compare(const void *a, const void *b);

ledEvent led_getNextEvent();
void led_init();
void led_shiftSend(uint16_t data);
#endif /* COLORMATH_H_ */
