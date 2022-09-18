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
#define STATE_BUT_PRESSED	0xFF
#define STATE_BUT_RELEASED	0
typedef struct
{
	uint8_t state;
	uint8_t	sample;
}button;
void but_init();
void but_start();
uint8_t but_getValue();

#endif /* BUTTON_H_ */