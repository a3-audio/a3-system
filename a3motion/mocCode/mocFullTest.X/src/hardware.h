/*
 * hardware.h
 *
 * Created: 17/03/2022 13:06:41
 *  Author: tirii
 */ 


#ifndef HARDWARE_H_
#define HARDWARE_H_
#define F_CPU 20000000UL

#define ENC_A_PT	PORTC	//PC1
#define ENC_A_BP	PIN1_bp
#define ENC_A_BM	PIN1_bm
#define ENC_B_PT	PORTB	//PB3
#define ENC_B_BP	PIN3_bp
#define ENC_B_BM	PIN3_bm
#define ENC_SW_PT	PORTA	//PA5
#define ENC_SW_BP	PIN5_bp
#define ENC_SW_BM	PIN5_bm
#define BU0_PT		PORTC	//PC3
#define BU0_BP		PIN3_bp
#define BU0_BM		PIN3_bm
#define BU0_STAT_BP	0
#define BU1_PT		PORTA	//PA4
#define BU1_BP		PIN4_bp
#define BU1_BM		PIN4_bm
#define BU1_STAT_BP	1
#define BU2_PT		PORTC	//PC0
#define BU2_BP		PIN0_bp
#define BU2_BM		PIN0_bm
#define BU2_STAT_BP	2
#define BU3_PT		PORTB	//PB4
#define BU3_BP		PIN4_bp
#define BU3_BM		PIN4_bm
#define BU3_STAT_BP	3
#define TWI_SDA_PT	PORTB	//PB1
#define TWI_SDA_BP	PIN1_bp
#define TWI_SDA_BM	PIN1_bm
#define TWI_SCL_PT	PORTB	//PB0
#define TWI_SCL_BP	PIN0_bp
#define TWI_SCL_BM	PIN0_bm
#define LED_SHU_PT	PORTB	//PB2
#define LED_SHU_BP	PIN2_bp
#define LED_SHU_BM	PIN2_bm
#define LED_SHD_PT	PORTA	//PA1
#define LED_SHD_BP	PIN1_bp
#define LED_SHD_BM	PIN1_bm
#define LED_SHC_PT	PORTA	//PA3
#define LED_SHC_BP	PIN3_bp
#define LED_SHC_BM	PIN3_bm
#define ADC0_PT	PORTA		//PA6
#define ADC0_BP	PIN6_bp
#define ADC0_BM	PIN6_bm
#define ADC1_PT	PORTB		//PB5
#define ADC1_BP	PIN5_bp
#define ADC1_PI	PIN5_bm

#define POS_LEDS1B	0
#define POS_LEDS1R	1
#define POS_LEDS1G	2
#define POS_LEDS2B	5
#define POS_LEDS2R	6
#define POS_LEDS2G	7
#define POS_LEDS3B	8
#define POS_LEDS3R	9
#define POS_LEDS3G	10
#define POS_LEDS4B	13
#define POS_LEDS4R	14
#define POS_LEDS4G	15




#endif /* HARDWARE_H_ */
