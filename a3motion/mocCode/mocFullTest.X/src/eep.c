#include "eep.h"

void eep_init() {
    eeprom_busy_wait();
    uint32_t eep_init_check = eeprom_read_dword(USER_ROW_TEST_ADDR); //read the test word
    if (USER_ROW_TEST_STRING != eep_init_check) { //test if the eeprom has been initialized
        eep_set_i2c_addr(1);
        eep_set_enc_step(1);

        eeprom_busy_wait(); //wait until the eeprom is ready
        eeprom_update_dword(USER_ROW_TEST_ADDR, USER_ROW_TEST_STRING); //first reads the value and only if it's different to the new a write occurs
    }

}

void eep_set_i2c_addr(uint8_t i2c_addr) {
    eeprom_busy_wait(); //wait until the eeprom is ready
    eeprom_update_byte(USER_ROW_I2C_ADDR, i2c_addr); //first reads the value and only if it's different to the new a write occurs
}

uint8_t eep_get_i2c_addr() {
    eeprom_busy_wait(); //wait until the eeprom is ready
    return eeprom_read_byte(USER_ROW_I2C_ADDR); //get the i2c address from eeprom 
}

void eep_set_enc_step(uint8_t enc_step) {
    eeprom_busy_wait(); //wait until the eeprom is ready
    eeprom_update_byte(USER_ROW_ENC_ADDR, enc_step); //first reads the value and only if it's different to the new a write occurs
}

uint8_t eep_get_enc_step() {
    eeprom_busy_wait(); //wait until the eeprom is ready
    return eeprom_read_byte(USER_ROW_ENC_ADDR); //get the i2c address from eeprom 
}
