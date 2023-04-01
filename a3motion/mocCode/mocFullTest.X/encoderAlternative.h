/* 
 * File:   encoderAlternative.h
 * Author: tiri
 *
 * Created on April 1, 2023, 2:10 PM
 */

#ifndef ENCODERALTERNATIVE_H
#define	ENCODERALTERNATIVE_H
#include "src\hardware.h"
void enc_init();
void enc_update();
void enc_setStep(uint8_t step);
int8_t enc_getValue();

#endif	/* ENCODERALTERNATIVE_H */

