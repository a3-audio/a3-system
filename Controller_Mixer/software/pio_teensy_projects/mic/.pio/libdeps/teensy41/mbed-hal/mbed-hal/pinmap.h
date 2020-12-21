/* mbed Microcontroller Library
 * Copyright (c) 2006-2015 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
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
#ifndef MBED_PINMAP_H
#define MBED_PINMAP_H

#include "PinNames.h"
#include "mbed-drivers/pinmap_common.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \defgroup hal_pin Pin hal functions
 * @{
 */

/** Set the pin function
 *
 * @param pin      The pin name
 * @param function The function value
 */
void pin_function(PinName pin, int function);

/** Set pin mode
 *
 * @param pin  The pin name
 * @param mode The pin mode to be set
 */
void pin_mode(PinName pin, PinMode mode);

/**@}*/

#ifdef __cplusplus
}
#endif

#endif
