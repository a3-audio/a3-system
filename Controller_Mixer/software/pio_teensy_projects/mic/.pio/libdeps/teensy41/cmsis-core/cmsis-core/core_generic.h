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

#ifndef __CMSIS_CORE_CORE_GENERIC_H__
#define __CMSIS_CORE_CORE_GENERIC_H__

#define __CMSIS_GENERIC
#if defined(TARGET_LIKE_CORTEX_M3)
  #include "cmsis-core/core_cm3.h"
#elif defined(TARGET_LIKE_CORTEX_M4)
  #include "cmsis-core/core_cm4.h"
#elif defined(TARGET_LIKE_CORTEX_M0)
  #include "cmsis-core/core_cm0.h"
#elif defined(TARGET_LIKE_CORTEX_M0PLUS)
  #include "cmsis-core/core_cm0plus.h"
#else
  #error "Unknown platform for core_generic.h"
#endif
#undef __CMSIS_GENERIC

#endif // #ifndef __CMSIS_CORE_CORE_GENERIC_H__

