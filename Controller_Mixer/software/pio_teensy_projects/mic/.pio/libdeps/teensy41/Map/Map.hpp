#ifndef MAP_H
#define MAP_H

#include "mbed.h"

/**
 *  A library that maps one range (inMin -> inMax) to another (outMin -> outMax)
 *
 * @author CA Bezuidenhout
 */
class Map
{
public:
  /**
   * @param inMin : Minimum value of input range
   * @param inMax : Maximum value of input range
   * @param outMin : Minimum value of output range
   * @param outMax : Maximum value of output range
   */
  Map(float inMin, float inMax, float outMin, float outMax);

  /**
   * Map inVal onto the output range
   *
   * @param inVal : A value in the input range to be mapped onto the output range
   * @returns A value in the output range
   */
  float Calculate(float inVal);
private:
  float _inMin,_inMax;
  float _outMin,_outMax;

};
#endif
