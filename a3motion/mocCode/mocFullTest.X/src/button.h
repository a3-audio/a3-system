/*
 * button.h
 *
 * Created: 22/03/2022 15:18:07
 *  Author: tirii
 */ 


#ifndef BUTTON_H_
#define BUTTON_H_
#define N_RGB_BUTTON	4
#include "hardware.h"
#include "bitoperation.h"
#include <avr/interrupt.h>
#include <avr/cpufunc.h> /* Required header file */
#define STATE_BUT_PRESSED	0xFF
#define STATE_BUT_RELEASED	0
typedef struct
{
	uint8_t state;
	uint8_t	sample;
}button;
void but_init();
void but_updateStates();
uint8_t but_getStates();

#endif /* BUTTON_H_ */