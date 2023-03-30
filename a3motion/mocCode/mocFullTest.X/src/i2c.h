/*
 * spi.h
 *
 * Created: 22/03/2022 15:11:23
 *  Author: tirii
 */ 


#ifndef SPI_H_
#define SPI_H_
#include "hardware.h"
#define I2C_MSG_FIRST_bm	(1<<7)
#define I2C_ORDER_READY_bm	(1<<7)
#define I2C_ORDER_READY_bp	7
#define I2C_CONVERT_MSG_to16(H,L)	(((H&0x7F)<<7)|(L&0x7F))	
typedef enum {stateIdle,stateADC0,stateEnc,stateBut,stateADC1,stateRGB0,stateRGB1,stateRGB2,stateRGB3}i2cState;
typedef enum {sendADC0,sendADC1,sendENC,sendBUT,i2cError}i2cResponse;
typedef enum {rqstADC0=11,rqstADC1=22,rqstENC=33,rqstBUT=44,setRGB0=55,setRGB1=66,setRGB2=77,setRGB3=88}i2cMessage;
typedef enum {idle,ordRgb0,ordRgb1,ordRgb2,ordRgb3}i2cOrder;
typedef struct{
	i2cOrder order;
	uint8_t msg[3];
	}i2cOrderStrct;
typedef struct{
	i2cResponse response;
	uint8_t index;
}i2cResponseStrct;

void i2c_init(uint8_t i2cAdrr);
//is called when the spi slave receives a message
void i2c_set_message(uint8_t msg);
//is called when the master requests data
//but doesn't contain the data but tells main what to fetch
i2cResponseStrct i2c_get_response();
//is called in main to execute order from master
i2cOrderStrct	i2c_get_order();


#endif /* SPI_H_ */