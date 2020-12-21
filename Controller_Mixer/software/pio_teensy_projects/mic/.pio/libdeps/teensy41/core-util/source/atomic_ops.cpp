/*
 * PackageLicenseDeclared: Apache-2.0
 * Copyright (c) 2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "core-util/atomic_ops.h"
#if defined(TARGET_LIKE_MBED)
#include "cmsis.h"
#endif

namespace mbed {
namespace util {

/* For ARMv7-M and above, we use the load/store-exclusive instructions to
 * implement atomic_cas, so we provide three template specializations
 * corresponding to the byte, half-word, and word variants of the instructions.
 */
#if (__CORTEX_M >= 0x03)

template<>
bool atomic_cas(uint8_t *ptr, uint8_t *expectedCurrentValue, uint8_t desiredValue)
{
    uint8_t currentValue = __LDREXB(ptr);
    if (currentValue != *expectedCurrentValue) {
        *expectedCurrentValue = currentValue;
        __CLREX();
        return false;
    }

    return !__STREXB(desiredValue, ptr);
}

template<>
bool atomic_cas(uint16_t *ptr, uint16_t *expectedCurrentValue, uint16_t desiredValue)
{
    uint16_t currentValue = __LDREXH(ptr);
    if (currentValue != *expectedCurrentValue) {
        *expectedCurrentValue = currentValue;
        __CLREX();
        return false;
    }

    return !__STREXH(desiredValue, ptr);
}

template<>
bool atomic_cas(uint32_t *ptr, uint32_t *expectedCurrentValue, uint32_t desiredValue)
{
    uint32_t currentValue = __LDREXW(ptr);
    if (currentValue != *expectedCurrentValue) {
        *expectedCurrentValue = currentValue;
        __CLREX();
        return false;
    }

    return !__STREXW(desiredValue, ptr);
}

template<>
uint8_t atomic_incr(uint8_t * valuePtr, uint8_t delta)
{
    uint8_t newValue;
    do {
        newValue = __LDREXB(valuePtr) + delta;
    } while (__STREXB(newValue, valuePtr));
    return newValue;
}
template<>
uint16_t atomic_incr(uint16_t * valuePtr, uint16_t delta)
{
    uint16_t newValue;
    do {
        newValue = __LDREXH(valuePtr) + delta;
    } while (__STREXH(newValue, valuePtr));
    return newValue;
}
template<>
uint32_t atomic_incr(uint32_t * valuePtr, uint32_t delta)
{
    uint32_t newValue;
    do {
        newValue = __LDREXW(valuePtr) + delta;
    } while (__STREXW(newValue, valuePtr));
    return newValue;
}

template<>
uint8_t atomic_decr(uint8_t * valuePtr, uint8_t delta)
{
    uint8_t newValue;
    do {
        newValue = __LDREXB(valuePtr) - delta;
    } while (__STREXB(newValue, valuePtr));
    return newValue;
}
template<>
uint16_t atomic_decr(uint16_t * valuePtr, uint16_t delta)
{
    uint16_t newValue;
    do {
        newValue = __LDREXH(valuePtr) - delta;
    } while (__STREXH(newValue, valuePtr));
    return newValue;
}

template<>
uint32_t atomic_decr(uint32_t * valuePtr, uint32_t delta)
{
    uint32_t newValue;
    do {
        newValue = __LDREXW(valuePtr) - delta;
    } while (__STREXW(newValue, valuePtr));
    return newValue;}

#endif /* #if (__CORTEX_M >= 0x03) */

} // namespace util
} // namespace mbed
