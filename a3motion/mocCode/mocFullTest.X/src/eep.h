/* 
 * File:   eep.h
 * Author: tiri
 *
 * Created on April 20, 2023, 11:37 PM
 */

#ifndef EEP_H
#define	EEP_H
#include <avr/eeprom.h>
#define USER_ROW_I2C_ADDR (uint8_t *)(0x1300-0x1400)
#define USER_ROW_ENC_ADDR (uint8_t *)(0x1301-0x1400)
#define USER_ROW_TEST_ADDR (uint32_t *)(0x1304-0x1400)
#define USER_ROW_TEST_STRING ((uint32_t)'t'<<24|(uint32_t)'s'<<16|(uint32_t)'e'<<8|(uint32_t)'t')

void eep_init();
void eep_set_i2c_addr(uint8_t i2c_addr);
uint8_t eep_get_i2c_addr();
uint8_t eep_get_enc_step();
void eep_set_enc_step(uint8_t enc_step);

#endif	/* EEP_H */

