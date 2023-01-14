/*
 * debug.h
 *
 * Created: 18/03/2022 10:25:53
 *  Author: tirii
 */ 


#ifndef DEBUG_H_
#define DEBUG_H_

void debug_init(){
	BITMASK_SET(ENC_SW_PT.DIR,ENC_SW_BM);
	BITMASK_SET(BU0_PT.DIR,BU0_BM);
}
void toggleDebugESW(){
	if(BITMASK_CHECK_ALL(ENC_SW_PT.OUT,ENC_SW_BM)){
		BITMASK_SET(ENC_SW_PT.OUTCLR,ENC_SW_BM);
		}else{
		BITMASK_SET(ENC_SW_PT.OUTSET,ENC_SW_BM);
	}
}

void toggleDebugBU0(){
	if(BITMASK_CHECK_ALL(BU0_PT.OUT,BU0_BM)){
		BITMASK_SET(BU0_PT.OUTCLR,BU0_BM);
		}else{
		BITMASK_SET(BU0_PT.OUTSET,BU0_BM);
	}
}



#endif /* DEBUG_H_ */