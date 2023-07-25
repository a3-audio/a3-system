/*
 * bitoperation.h
 *
 * Created: 17/03/2022 13:08:54
 *  Author: tirii
 */ 


#ifndef BITOPERATION_H_
#define BITOPERATION_H_

#define BIT_SET(a,b) ((a) |= (1<<(b)))
#define BIT_CLEAR(a,b) ((a) &= ~(1<<(b)))
#define BIT_FLIP(a,b) ((a) ^= (1<<(b)))
#define BIT_CHECK(a,b) (!!((a) & (1<<(b))))        // '!!' to make sure this returns 0 or 1
#define BITMASK_SET(x, mask) ((x) |= (mask))
#define BITMASK_CLEAR(x, mask) ((x) &= (~(mask)))
#define BITMASK_FLIP(x, mask) ((x) ^= (mask))
#define BITMASK_CHECK_ALL(x, mask) (!(~(x) & (mask)))
#define BITMASK_CHECK_ANY(x, mask) ((x) & (mask))




#endif /* BITOPERATION_H_ */
