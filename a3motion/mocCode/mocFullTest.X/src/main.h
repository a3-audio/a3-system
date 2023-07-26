/*
 * main.h
 *
 * Created: 27/02/2022 00:02:29
 *  Author: tirii
 */ 


#ifndef MAIN_H_
#define MAIN_H_
#include <avr/interrupt.h>
#include "hardware.h"
#include "bitoperation.h"
#include "ledandcolor.h"
#include "button.h"
#include "encoderAlternative.h"
#include "timer.h"
#include "adc.h"
#include "i2cAlternative.h"
#include <avr/cpufunc.h> /* Required header file */
#include "eep.h"
typedef struct{
    uint8_t button;
    uint16_t adc0;
    uint16_t adc1;
    uint8_t encoder;
} sensor;



void led_shiftSend(uint16_t data);
int8_t encode_read( uint8_t step );

 //converts an angle and a intensity value to RGB
 //angle is 0-360 and val 0-255

#endif /* MAIN_H_ */
