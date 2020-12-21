/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
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
#include "core-util/sbrk.h"

#include <stdlib.h>

void * volatile mbed_krbs_ptr     = MBED_KRBS_START;
void * volatile mbed_sbrk_ptr     = MBED_SBRK_START;
volatile ptrdiff_t mbed_sbrk_diff = MBED_HEAP_SIZE;

void * mbed_sbrk(ptrdiff_t size)
{
    if (size == 0) {
        return (void *) mbed_sbrk_ptr;
    }

    // align absolute size requested
    ptrdiff_t size_internal = abs(size);
    if ((uintptr_t)size_internal < SBRK_INC_MIN) {
            size_internal = SBRK_INC_MIN;
    }
    size_internal = ( size_internal + SBRK_ALIGN - 1) & ~(SBRK_ALIGN - 1);
    // it's min sized plus aligned, assign back the sign
    if (size < 0) {
        size_internal = -size_internal;
    }

    /* Decrement mbed_sbrk_diff by the size being allocated. */
    ptrdiff_t ptr_diff = mbed_sbrk_diff;
    while (1) {
        if (size_internal > ptr_diff) {
            return (void *) -1;
        }
        if (mbed::util::atomic_cas((uint32_t *)&mbed_sbrk_diff, (uint32_t *)&ptr_diff, (uint32_t)(ptr_diff - size_internal))) {
            break;
        }
    }

    uintptr_t new_sbrk_ptr = mbed::util::atomic_incr((uint32_t *)&mbed_sbrk_ptr, (uint32_t)size_internal);
    return (void *)(new_sbrk_ptr - size_internal);
}

void * mbed_krbs(const ptrdiff_t size)
{
    return mbed_krbs_ex(size, NULL);
}

void * mbed_krbs_ex(const ptrdiff_t size, ptrdiff_t *actual)
{
    if (size == 0) {
        return (void *) mbed_krbs_ptr;
    }
    // krbs does not support deallocation.
    if (size < 0) {
        return (void *) -1;
    }

    uintptr_t size_internal = (uintptr_t)size;
    // Guarantee minimum allocation size
    if (size_internal < KRBS_INC_MIN) {
        size_internal = KRBS_INC_MIN;
    }
    size_internal = (size_internal + KRBS_ALIGN - 1) & ~(KRBS_ALIGN - 1);

    /* Decrement mbed_sbrk_diff by the size being allocated. */
    ptrdiff_t ptr_diff = mbed_sbrk_diff;
    while (1) {
        if ((size_internal > (uintptr_t)ptr_diff) && (actual == NULL)) {
            return (void *) -1;
        }
        if (mbed::util::atomic_cas((uint32_t *)&mbed_sbrk_diff, (uint32_t *)&ptr_diff, (uint32_t)(ptr_diff - size_internal))) {
            break;
        }
    }

    return (void *)mbed::util::atomic_decr((uint32_t *)&mbed_krbs_ptr, (uint32_t)size_internal);
}
