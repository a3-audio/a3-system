

/* 
 * File:   
 * Author: 
 * Comments:
 * Revision history: 
 */

// This is a guard condition so that contents of this file are not included
// more than once.  
#ifndef DATA_HEADER_TEMPLATE_H
#define	DATA_HEADER_TEMPLATE_H

#include <xc.h> // include processor files - each processor file is guarded.  
typedef struct data{
    uint16_t adc0=0;
    uint16_t adc1=1;
    int8_t encoder=0;
    uint8_t button=0;
}data;





#endif	/* XC_HEADER_TEMPLATE_H */

