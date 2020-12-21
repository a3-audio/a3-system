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
#ifndef __MBED_ALLOC_H
#define __MBED_ALLOC_H

#include <stddef.h>

#if defined(__ARMCC_VERSION)
#   include <rt_sys.h>
#   define PREFIX(x)    _sys##x
#   define OPEN_MAX     _SYS_OPEN
#   ifdef __MICROLIB
#       pragma import(__use_full_stdio)
#   endif

#elif defined(__ICCARM__)
#   include <yfuns.h>
#   define PREFIX(x)        _##x
#   define OPEN_MAX         16

#   define STDIN_FILENO     0
#   define STDOUT_FILENO    1
#   define STDERR_FILENO    2

#else
#   ifndef TARGET_LIKE_POSIX
#       include <sys/syslimits.h>
#   else
#       include <stddef.h>
#   endif
#   define PREFIX(x)    x
#endif

#ifndef pid_t
 typedef int pid_t;
#endif
#ifndef caddr_t
 typedef char * caddr_t;
#endif

#ifndef SBRK_ALIGN
#define SBRK_ALIGN 8U
#endif
#if (SBRK_ALIGN & (SBRK_ALIGN-1))
#error SBRK_ALIGN must be a power of 2
#endif

#ifndef SBRK_INC_MIN
#define SBRK_INC_MIN (SBRK_ALIGN)
#endif

#ifndef KRBS_ALIGN
#define KRBS_ALIGN 8U
#endif
#if (KRBS_ALIGN & (KRBS_ALIGN-1))
#error KRBS_ALIGN must be a power of 2
#endif

#ifndef KRBS_INC_MIN
#define KRBS_INC_MIN (KRBS_ALIGN)
#endif

/**
 * Here's a picture to explain the mbed OS memory layout. It should help with
 * some of the concepts below.
 *
 *            | inaccessible |
 *            | or RAM-end   |
 * high addrs +--------------+  +--+--+
 *            |  krbs_start  |     |
 *            |      +       |     |
 *            |      |       |     |
 *            |      |       |     |
 *            |      v       |     |
 *            |              |     |
 *            |  Free store  |  heap_size
 *            |              |     |
 *            |      ^       |     |
 *            |      |       |     |
 *            |      |       |     |
 *            |      +       |     |
 *            |  sbrk_start  |     |
 *            +--------------+  +--+--+
 *            |              |
 *            |   BSS        |
 *            |              |
 *            +--------------+
 *            |              |
 *            |   Data       |
 *            |              |
 *            +---------+----+
 *            |         |    |
 *            |   stack |    |
 *            |         v    |
 *            |              |
 *  low addrs +--------------+
 *            | inaccessible |
 *            | or RAM-start |
 */

/**
 * __heap_size is a symbol defined by the yotta target to contain the size of
 * the free-store. In mbed OS, this is typically defined in the linker script
 * associated with the target. The value is resolved at link time and is
 * available within the program using the const R-value expression `&__heap_size`.
 *
 * For some targets, __heap_size may also be given a value programmatically by
 * the application during system startup; in this case, it is available
 * as a regular extern const L-value symbol.
 *
 * The macro MBED_HEAP_SIZE adds a level of indirection to abstract __heap_size.
 */
#ifndef MBED_HEAP_SIZE
#   ifndef TARGET_LIKE_POSIX
#       ifdef __ARMCC_VERSION
#           define __heap_size (Image$$ARM_LIB_HEAP$$ZI$$Length)
#       endif
        extern unsigned int __heap_size;
#       define MBED_HEAP_SIZE ((ptrdiff_t)&__heap_size)
#   else
        extern unsigned int __heap_size;
#       define MBED_HEAP_SIZE ((ptrdiff_t) __heap_size)
#   endif
#endif /* #ifndef MBED_HEAP_SIZE */

/**
 * The symbols __mbed_sbrk_start and __mbed_krbs_start are defined by the yotta-
 * target to mark the boundary of the free-store. In mbed OS, these are
 * typically defined in the linker script associated with the target. The
 * values are resolved at link time and are available within the program using
 * toolchain specific const R-value expressions.
 *
 * For some targets, sbrk_start and krbs_start may also be given a value
 * programmatically by the application during system startup; in this case,
 * these are available as a regular extern const L-value symbols.
 *
 * The macros MBED_SBRK_START and MBED_KRBS_START add a level of indirection to
 * abstract these symbols.
 */
#if !defined(MBED_SBRK_START) || !defined(MBED_KRBS_START)
#   ifndef TARGET_LIKE_POSIX
#       ifdef __ARMCC_VERSION
#           define __mbed_sbrk_start (Image$$ARM_LIB_HEAP$$Base)
#           define __mbed_krbs_start (Image$$ARM_LIB_HEAP$$ZI$$Limit)
#           pragma import(__use_two_region_memory)
#       endif /* #ifdef __ARMCC_VERSION */
        extern unsigned int __mbed_sbrk_start;
        extern unsigned int __mbed_krbs_start;
#       define MBED_SBRK_START &__mbed_sbrk_start
#       define MBED_KRBS_START &__mbed_krbs_start
#   else /* #ifdef TARGET_LIKE_POSIX */
        extern void *__mbed_sbrk_start;
        extern void *__mbed_krbs_start;
#       define MBED_SBRK_START __mbed_sbrk_start
#       define MBED_KRBS_START __mbed_krbs_start
#   endif /* #ifdef TARGET_LIKE_POSIX */
#endif

#ifdef __cplusplus
extern "C" {
#endif
void * mbed_sbrk(ptrdiff_t size);
void * mbed_krbs(const ptrdiff_t size);
void * mbed_krbs_ex(const ptrdiff_t size, ptrdiff_t *actual);
#ifdef __cplusplus
}
#endif


#endif // __MBED_ALLOC_H
