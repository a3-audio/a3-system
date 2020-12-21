/*
 * PackageLicenseDeclared: Apache-2.0
 * Copyright (c) 2015-2016 ARM Limited
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
#ifndef __CORE_UTIL_UNINITIALIZED_H__
#define __CORE_UTIL_UNINITIALIZED_H__

/**
 * The following macros are used to place uninitialized data in a dedicated
 * section, which is not touched by the C/C++ library at startup time. They can
 * be used, for example, to hold data and state across reboots.
 *
 * Note: These macros require additional support from the platform linker
 * script.
 *
 * In GCC:
 *      .uninitialized (NOLOAD):
 *      {
 *          . = ALIGN(32);
 *          __uninitialized_start = .;
 *          *(.uninitialized)
 *          KEEP(*(.keep.uninitialized))
 *          . = ALIGN(32);
 *          __uninitialized_end = .;
 *      } > RAM
 *
 *  In ARMCC:
 *      ER_UNINITIALIZED +0 UNINIT NOCOMPRESS
        {
            * (.keep.uninitialized)
            * (.uninitialized)
        }
 *  which also requires an additional linker option:
 *      set(CMAKE_EXE_LINKER_FLAGS_INIT
 *          "${CMAKE_EXE_LINKER_FLAGS_INIT} --keep=\"*(.keep*)\"")
 *  to make sure that unused symbols are not discarded. The GNU extensions must
 *  be enabled (--gnu).
 */

#if defined(__GNUC__) || defined (__CC_ARM) || defined(__clang__)

#ifndef __uninitialized
    #define __uninitialized __attribute__((section(".uninitialized")))
#endif

#ifndef __force_uninitialized
    #define __force_uninitialized __attribute__((section(".keep.uninitialized")))
#endif

#else

#error "This compiler is not yet supported by core-util/uninitialized.h."

#endif /* defined(__GNUC__) || defined (__CC_ARM) || defined(__clang__) */

#endif /* __CORE_UTIL_UNINITIALIZED_H__ */
