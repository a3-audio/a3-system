#include "Map.hpp"

Map::Map(float inMin, float inMax, float outMin, float outMax)
{
  _inMin = inMin;
  _inMax = inMax;
  _outMin = outMin;
  _outMax = outMax;
}

float Map::Calculate(float inVal)
{
  return ( (inVal - _inMin)*(_outMax - _outMin)/(_inMax - _inMin) + _outMin );
}
