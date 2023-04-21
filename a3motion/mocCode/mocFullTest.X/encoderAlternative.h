/* 
 * File:   encoderAlternative.h
 * Author: tiri
 *
 * Created on April 1, 2023, 2:10 PM
 */

#ifndef ENCODERALTERNATIVE_H
#define	ENCODERALTERNATIVE_H
#include "src\hardware.h"
#include "src\bitoperation.h"
#include <avr/interrupt.h>
void enc_init(uint8_t enc_step);
void enc_update();
void enc_set_step(uint8_t step);
int8_t enc_getValue();

#endif	/* ENCODERALTERNATIVE_H */

