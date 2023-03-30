
#ifndef XC_HEADER_TEMPLATE_H
#define	XC_HEADER_TEMPLATE_H

//#include <xc.h> // include processor files - each processor file is guarded.
#include "src/bitoperation.h"
#include "main.h"
#include <stdlib.h>
// I2C slave command macros
#define I2C_complete() TWI0.SCTRLB = TWI_SCMD_COMPTRANS_gc
#define I2C_response() TWI0.SCTRLB = TWI_SCMD_RESPONSE_gc
#define I2C_sendACK()  TWI0.SCTRLB = TWI_ACKACT_ACK_gc  | TWI_SCMD_RESPONSE_gc
#define I2C_sendNACK() TWI0.SCTRLB = TWI_ACKACT_NACK_gc | TWI_SCMD_RESPONSE_gc
#define I2C_put(x)     TWI0.SDATA  = (x)
#define I2C_get()      TWI0.SDATA

// I2C slave status macros
#define I2C_isAddr()  ((TWI0.SSTATUS & TWI_APIF_bm) && (TWI0.SSTATUS & TWI_AP_bm))
#define I2C_isData()  (TWI0.SSTATUS & TWI_DIF_bm)
#define I2C_isStop()  ((TWI0.SSTATUS & TWI_APIF_bm) && (~TWI0.SSTATUS & TWI_AP_bm))
#define I2C_isIn()    (~TWI0.SSTATUS & TWI_DIR_bm)
#define I2C_isOut()   (TWI0.SSTATUS & TWI_DIR_bm)

#define I2C_msg_setLed 42
#define I2C_state_setLed1 43
#define I2C_state_setLed2 44
#define I2C_state_idle 0

extern void i2c_init(uint8_t i2cAdrr);
extern void i2c_interrupt();

extern uint8_t getSensorData(uint8_t i);
extern void setLedData(uint8_t button_i,uint8_t r,uint8_t g,uint8_t b);
#endif	/* XC_HEADER_TEMPLATE_H */

