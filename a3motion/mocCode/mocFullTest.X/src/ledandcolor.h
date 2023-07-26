/*
 * colormath.h
 *
 * Created: 16/03/2022 13:13:26
 *  Author: tirii
 */ 


#ifndef COLORMATH_H_
#define COLORMATH_H_
#include "hardware.h"
#include "bitoperation.h"
#include	<stdbool.h>
#include <avr/io.h>
#include <stdlib.h>
#define LED_MAX 63


typedef struct{
	uint16_t shift;
	uint8_t time;
} ledEvent;


typedef struct{
	uint8_t	hw_position;
	uint8_t time;
}led;


typedef struct
 {
	 uint8_t *r;
	 uint8_t *g;
	 uint8_t *b;
 }rgbLed;
 
void led_updateRGB(uint8_t number,uint8_t r,uint8_t g,uint8_t b);
void led_rgbInit();
ledEvent led_updateColorSystem();
int led_Compare(const void *a, const void *b);

ledEvent led_getNextEvent();
void led_init();
void led_shiftSend(uint16_t data);
#endif /* COLORMATH_H_ */
