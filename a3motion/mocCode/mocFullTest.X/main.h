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
#include "src/debug.h"
#include "src/button.h"
#include "encoderAlternative.h"
#include "src/timer.h"
#include "src/adc.h"
#include "i2cAlternative.h"
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
