 
 #include "i2c.h"


 i2cState state=stateIdle;
 i2cOrderStrct orderBuffer[5];
 uint8_t s_orderBuffer=-1;
 uint8_t	n_orders=0;
 uint8_t	rxBuffer[3];
 uint8_t n_rxBuffer=0;
 uint8_t i_txBuffer=0;
 /*
 Initialize the SPI to a basic functional state by following these steps:
 1. Configure the SS pin in the port peripheral.
 2. Select SPI master/slave operation by writing the Master/Slave Select bit (MASTER) in the Control A register
 (SPIn.CTRLA).
 3. In Master mode, select the clock speed by writing the Prescaler bits (PRESC) and the Clock Double bit
 (CLK2X) in SPIn.CTRLA.
 4. Optional: Select the Data Transfer mode by writing to the MODE bits in the Control B register (SPIn.CTRLB).
 5. Optional: Write the Data Order bit (DORD) in SPIn.CTRLA.
 6. Optional: Setup Buffer mode by writing BUFEN and BUFWR bits in the Control B register (SPIn.CTRLB).
 7. Optional: To disable the multi-master support in Master mode, write �1� to the Slave Select Disable bit (SSD) in
 SPIn.CTRLB.
 8. Enable the SPI by writing a �1� to the ENABLE bit in SPIn.CTRLA.
 */
 void i2c_init(uint8_t i2cAddr)
 {
	 TWI0.SADDR = (i2cAddr<<1)|0x01;			//Slave address & enable general call
	 TWI0.SCTRLA = TWI_ENABLE_bm |	    //Enable slave peripheral
	 TWI_APIEN_bm |		//Enable address match interrupt
	 TWI_PIEN_bm |			//Enable stop interrupt
	 TWI_DIEN_bm |			//Enable data interrupt
	 TWI_SMEN_bm;			//Enable smart mode
	 orderBuffer[0].order=ordRgb0;
	 orderBuffer[1].order=ordRgb1;
	 orderBuffer[2].order=ordRgb2;
	 orderBuffer[3].order=ordRgb3;
 }

 void i2c_set_message(uint8_t msg){
	 if(BITMASK_CHECK_ALL(msg,I2C_MSG_FIRST_bm)){
		 if(state==stateIdle){
		 BITMASK_CLEAR(msg,I2C_MSG_FIRST_bm);
		 i_txBuffer=0;
		 n_rxBuffer=0;
		 s_orderBuffer=-1;
		 switch(msg){
			 case rqstADC0:
			 state=stateADC0;
			 break;
			 case rqstADC1:
			 state=stateADC1;
			 break;
			 case rqstENC:
			 state=stateEnc;
			 break;
			 case rqstBUT:
			 state=stateBut;
			 break;
			 case setRGB0:
			 if(!BIT_CHECK(orderBuffer[0].order,I2C_ORDER_READY_bp)){
			 s_orderBuffer=0;
			 state=stateRGB0;
			 }
			 break;
			 case setRGB1:
			 if(!BIT_CHECK(orderBuffer[1].order,I2C_ORDER_READY_bp)){
			 s_orderBuffer=1;
			 state=stateRGB1;
			 }
			 break;
			 case setRGB2:
			 if(!BIT_CHECK(orderBuffer[2].order,I2C_ORDER_READY_bp)){
			 s_orderBuffer=2;
			 state=stateRGB2;
			 }
			 break;
			 case setRGB3:
			  if(!BIT_CHECK(orderBuffer[3].order,I2C_ORDER_READY_bp)){
			 s_orderBuffer=3;
			 state=stateRGB3;
			  }
			 break;
		 }
		 }
		 }else{
		 switch(state){
			 case stateRGB0:
			 case stateRGB1:
			 case stateRGB2:
			 case stateRGB3:
			 orderBuffer[s_orderBuffer].msg[n_rxBuffer]=msg;
			 n_rxBuffer++;
			 //the order is ready
			 if(n_rxBuffer>=3){
				 BIT_SET(orderBuffer[s_orderBuffer].order,I2C_ORDER_READY_bp);
				 state=stateIdle;
			 }
			 break;
			 default:
			 n_rxBuffer=0;
			 state=stateIdle;
			 break;
		 }
	 }
 }
 i2cResponseStrct i2c_get_response(){
	 i2cResponseStrct responseState;
	 switch (state)
	 {
		 case stateADC0:
		 responseState.response=sendADC0;
		 responseState.index=i_txBuffer++;
		 if(i_txBuffer>=2){
			 i_txBuffer=0;
			 state=stateIdle;
		 }
		 break;
		 case stateADC1:
		 responseState.response=sendADC1;
		 responseState.index=i_txBuffer++;
		 if(i_txBuffer>=2){
			 i_txBuffer=0;
			 state=stateIdle;
		 }
		 break;
		 case stateEnc:
		 responseState.response=sendENC;
		 responseState.index=i_txBuffer++;
		 if(i_txBuffer>=2){
			 i_txBuffer=0;
			 state=stateIdle;
		 }
		 break;
		 case stateBut:
		 responseState.response=sendBUT;
		 i_txBuffer=0;
		 state=stateIdle;
		 break;
		 //a byte was requested but we don't know which
		 default:
		 i_txBuffer=0;
		 responseState.response=i2cError;
		 state=stateIdle;
		 break;
	 }
	 return responseState;
 }
 
 i2cOrderStrct	i2c_get_order(){
	 i2cOrderStrct retVal;
	 retVal.order=-1;
	 for (int i=0;i<5;i++)
	 {
		 //do we have an order ready
		 cli();
		 if (BIT_CHECK(orderBuffer[i].order,I2C_ORDER_READY_bp))
		 {
			 BIT_CLEAR(orderBuffer[i].order,I2C_ORDER_READY_bp);
			 retVal=orderBuffer[i];
			 sei();
			 return retVal;
		 }
		 sei();
	 }
	 return retVal;
	 
 }