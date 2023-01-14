/*
 * encoder.h
 *
 * Created: 22/03/2022 15:17:41
 *  Author: tirii
 */ 


#ifndef ENCODER_H_
#define ENCODER_H_

#include "hardware.h"

void enc_init();
void enc_start();
int16_t enc_getValue();


#endif /* ENCODER_H_ */